from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

def load_model():
    model_name = "sshleifer/distilbart-cnn-12-6"
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
        max_length=500,
        num_beams=5,
        no_repeat_ngram_size=2,
        do_sample=True,  # Enable sampling to use top_k and top_p
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = generated_text[len(question):].strip()
    return response

if __name__ == "__main__":
    model, tokenizer, device = load_model()
    question = "write a script to print hello world in python"
    answer = generate_answer(model, tokenizer, device, question)
    print(answer)
