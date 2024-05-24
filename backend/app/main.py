import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .fetch_web_content import fetch_web_content  # Ensure these modules are available
from .data_cleaning import extract_relevant_paragraphs  # Ensure these modules are available
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch

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

    response = question_answerer(question=question.question, context=summarized_content)
    logger.info("Generated answer: %s", response['answer'])
    
    return {"answer": response['answer']}
