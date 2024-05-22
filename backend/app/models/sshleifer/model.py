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

def is_model_ready():
    try:
        model, tokenizer, device = load_model()
        return model is not None and tokenizer is not None and device is not None
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def generate_answer(model, tokenizer, device, question):
    context = "Scuderia Ferrari is the racing division of luxury Italian auto manufacturer Ferrari and the racing team that competes in Formula One racing. The team was founded by Enzo Ferrari, initially to race cars produced by Alfa Romeo, though by 1947 Ferrari had begun building its own cars. Scuderia Ferrari is the oldest surviving and most successful Formula One team, having competed in every world championship since the 1950 Formula One season. The team holds the most constructors' championships, with a record 16 titles, and has produced numerous successful drivers, including world champions like Alberto Ascari, Niki Lauda, and Michael Schumacher. The team's iconic red cars, known as 'Prancing Horse', have become a symbol of speed, engineering excellence, and a rich racing heritage. The Ferrari F1 team is based in Maranello, Italy, and continues to be a major competitor in Formula One, often pushing the boundaries of automotive technology and design."
    combined_input = f"question: {question} context: {context}"
    inputs = tokenizer(combined_input, return_tensors="pt")
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
    response = generated_text.strip()
    return response
