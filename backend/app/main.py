from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Message(BaseModel):
    message: str

# Load the GPT-2 model and tokenizer
model_name = "gpt2-xl"
print(f"gpu available: {torch.cuda.is_available()}")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

@app.post("/api/chat")
async def chat(message: Message):
    inputs = tokenizer(message.message, return_tensors="pt")
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=150,  # Adjust max_length for more reasonable response size
        num_beams=5,  # Use beam search for better results
        no_repeat_ngram_size=2,  # Avoid repeating the same n-grams
        top_k=50,  # Top-k sampling
        top_p=0.95,  # Top-p (nucleus) sampling
        pad_token_id=tokenizer.eos_token_id
    )
    # Decode the generated response and trim the input prompt from the beginning
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Remove the input prompt from the beginning of the response
    response = generated_text[len(message.message):].strip()
    return {"reply": response}

