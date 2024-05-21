from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.models.distilbart_cnn_12_6.model import load_model, generate_answer

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
print("Loading model...")
model, tokenizer, device = load_model()
model_ready = model is not None and tokenizer is not None and device is not None
print("Model loaded successfully." if model_ready else "Model failed to load.")

@app.get("/api/health")
async def health_check():
    return {"status": "ready" if model_ready else "not ready"}

@app.post("/api/ask")
async def ask_question(question: Question):
    if not model_ready:
        return {"error": "Model is not ready"}
    print(f"Question: {question.question}")
    response = generate_answer(model, tokenizer, device, question.question)
    return {"answer": response}
