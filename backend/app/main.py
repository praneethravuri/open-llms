import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .fetch_web_content import fetch_web_content
from .data_cleaning import extract_relevant_paragraphs
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch
import language_tool_python
from textblob import TextBlob 

# Set environment variables
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

print(torch.cuda.is_available())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str
    model: str
    

def correct_grammar(text):
    # tool = language_tool_python.LanguageTool('en-US')
    # result = tool.correct(text)
    
    text = TextBlob(text)
    corrected_text = text.correct()
    print(f"Corrected Text: {corrected_text}")
    print(f"Type of detailed answers: {type(corrected_text)}")
    return str(corrected_text)
    
@app.get("/api/server-status")
def read_root():
    logger.info("Server status requested")
    return {"message": "Server is running"}

@app.post("/api/ask")
async def ask_question(question: Question):
    logger.info("Received question: %s", question.question)
    sentence_transformer_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1', device='cuda')

    paragraphs = fetch_web_content(question.question)
    relevant_paragraphs = extract_relevant_paragraphs(paragraphs=paragraphs, question=question.question, model=sentence_transformer_model)
    if not relevant_paragraphs:
        logger.warning("No relevant content found for question: %s", question.question)
        raise HTTPException(status_code=404, detail="No relevant web content found for the question.")
    summarized_content = "".join(relevant_paragraphs)
    if not summarized_content.strip():
        logger.warning("Summarization resulted in empty content for question: %s", question.question)
        raise HTTPException(status_code=404, detail="Summarization resulted in empty content.")
    
    model_name = question.model
    question_answerer = pipeline(
        "question-answering", 
        model=AutoModelForQuestionAnswering.from_pretrained(model_name), 
        tokenizer=AutoTokenizer.from_pretrained(model_name),
        device=0  # Use GPU if available
    )

    # Generate multiple answers
    responses = []
    for start in range(0, len(summarized_content), 1024):
        part = summarized_content[start:start + 1024]
        response = question_answerer(question=question.question, context=part, max_answer_len=1024, batch_size=16)
        if 'answer' in response and response['answer']:
            responses.append(response['answer'])

    # Combine answers to form a detailed response
    detailed_answer = " ".join(responses)
    if not detailed_answer.strip():
        logger.warning("Generated answer is empty for question: %s", question.question)
        raise HTTPException(status_code=404, detail="Generated answer is empty.")

    logger.info("Generated answer: %s", detailed_answer)
    
    print(f"\n\n\n\nType of detailed answers: {type(detailed_answer)}")
    
    print(f"\n\n\nGenerated Answers : {detailed_answer}")
    
    grammar_corrected_answer = correct_grammar(text=detailed_answer)
    
    return {"answer": grammar_corrected_answer}
