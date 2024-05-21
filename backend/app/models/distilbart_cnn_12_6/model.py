from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

def load_model():
    model_name = "sshleifer/distilbart-cnn-12-6"  # Path to the saved model
    print(f"GPU available: {torch.cuda.is_available()}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer, device

def generate_answer(model, tokenizer, device, question):
    inputs = tokenizer(question, return_tensors="pt")
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=100,  # Adjust max_length for more reasonable response size
        num_beams=5,  # Use beam search for better results
        no_repeat_ngram_size=2,  # Avoid repeating the same n-grams
        top_k=50,  # Top-k sampling
        top_p=0.95,  # Top-p (nucleus) sampling
        pad_token_id=tokenizer.eos_token_id
    )
    # Decode the generated response and trim the input prompt from the beginning
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Remove the input prompt from the beginning of the response
    response = generated_text[len(question):].strip()
    return response