from transformers import AutoTokenizer, BartForConditionalGeneration

def chunk_text(text, chunk_size=512):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def summarize_content(content):
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)
    model = model.to('cuda')  # Ensure model is on GPU

    summaries = []
    for chunk in chunk_text(content):
        inputs = tokenizer(chunk, max_length=1024, return_tensors="pt", truncation=True)
        inputs = {key: value.to('cuda') for key, value in inputs.items()}  # Move inputs to GPU
        summary_ids = model.generate(inputs["input_ids"], num_beams=4, max_length=150, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    print(f"Summarized content: {' '.join(summaries)}")
    return ' '.join(summaries)
