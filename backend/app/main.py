import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .fetch_web_content import fetch_web_content
from .data_cleaning import extract_relevant_paragraphs
from .data_summarization import summarize_content
from transformers import pipeline, AutoTokenizer
from sentence_transformers import SentenceTransformer


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

@app.get("/api/server-status")
def read_root():
    logger.info("Server status requested")
    return {"message": "Server is running"}

@app.post("/api/ask")
async def ask_question(question: Question):
    logger.info("Received question: %s", question.question)
    context = ""
    model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1', device='cuda')
    
    paragraphs = fetch_web_content(question.question)
    relevant_paragraphs = extract_relevant_paragraphs(paragraphs=paragraphs, question=question.question, model=model)
    summarized_content = summarize_content(' '.join(relevant_paragraphs))
    context += summarized_content + " "

    if not context:
        logger.warning("No relevant content found for question: %s", question.question)
        raise HTTPException(status_code=404, detail="No relevant web content found for the question.")
    
    question_answerer = pipeline(
        "question-answering", 
        model="Intel/dynamic_tinybert", 
        tokenizer=AutoTokenizer.from_pretrained("Intel/dynamic_tinybert"),
        device=0
    )

    response = question_answerer(question=question.question, context=context, max_length=500, min_length=100)
    logger.info("Generated answer: %s", response['answer'])
    
    return {"answer": response['answer']}
