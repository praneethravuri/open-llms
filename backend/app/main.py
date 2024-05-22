from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .fetch_web_content import fetch_web_content
from .data_cleaning import extract_relevant_paragraphs
from .data_summarization import summarize_content
from transformers import pipeline, AutoTokenizer
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Question(BaseModel):
    question: str

@app.get("/api/server-status")
def read_root():
    return {"message": "Server is running"}

@app.post("/api/ask")
async def ask_question(question: Question):
    context = ""
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
    
    paragraphs = fetch_web_content(question.question)
    relevant_paragraphs = extract_relevant_paragraphs(paragraphs=paragraphs, question=question.question, model=model)
    summarized_content = summarize_content(' '.join(relevant_paragraphs))
    context += summarized_content + " "

    if not context:
        raise HTTPException(status_code=404, detail="No relevant web content found for the question.")
    
    question_answerer = pipeline(
        "question-answering", 
        model="Intel/dynamic_tinybert", 
        tokenizer=AutoTokenizer.from_pretrained("Intel/dynamic_tinybert"),
        device=0  # Ensure it uses the GPU
    )

    response = question_answerer(question=question.question, context=context, max_length = 500, min_length = 100)
    
    return {"answer": response['answer']}
