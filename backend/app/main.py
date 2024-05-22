from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import importlib

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
    model: str

model_modules = {
    "deepset/tinyroberta-squad2": "app.models.deepset.tinyroberta_squad2.model",
    "sshleifer/distilbart-cnn-12-6": "app.models.sshleifer.distilbart_cnn_12_6.model"
}

@app.post("/api/ask")
async def ask_question(question: Question):
    if question.model not in model_modules:
        raise HTTPException(status_code=400, detail="Invalid model specified")

    model_module = importlib.import_module(model_modules[question.model])
    model, tokenizer, device = model_module.load_model()
    
    if not model:
        raise HTTPException(status_code=503, detail="Model is not ready")

    response = model_module.generate_answer(model, tokenizer, device, question.question)
    return {"answer": response}
