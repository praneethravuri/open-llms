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
    context = "Scuderia Ferrari is the racing division of luxury Italian auto manufacturer Ferrari and the racing team that competes in Formula One racing. The team was founded by Enzo Ferrari, initially to race cars produced by Alfa Romeo, though by 1947 Ferrari had begun building its own cars. Scuderia Ferrari is the oldest surviving and most successful Formula One team, having competed in every world championship since the 1950 Formula One season. The team holds the most constructors' championships, with a record 16 titles, and has produced numerous successful drivers, including world champions like Alberto Ascari, Niki Lauda, and Michael Schumacher. The team's iconic red cars, known as 'Prancing Horse', have become a symbol of speed, engineering excellence, and a rich racing heritage. The Ferrari F1 team is based in Maranello, Italy, and continues to be a major competitor in Formula One, often pushing the boundaries of automotive technology and design."
    response = generate_answer(model, tokenizer, device, question.question, context=context)
    return {"answer": response}
