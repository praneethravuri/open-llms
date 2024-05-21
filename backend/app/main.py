from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.models.distilbart_cnn_12_6.model import load_model, generate_answer
import torch

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

# Load model and tokenizer
model, tokenizer, device = load_model()

@app.post("/api/ask")
async def ask_question(question: Question):
    print(f"Question: {question.question}")
    response = generate_answer(model, tokenizer, device, question.question)
    return {"answer": response}
