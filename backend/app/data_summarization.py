from transformers import AutoTokenizer, T5ForConditionalGeneration
import logging

logger = logging.getLogger(__name__)

def chunk_text(text, chunk_size=512):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def summarize_content(content):
    model_name = "t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model = model.to('cuda')

    summaries = []
    for chunk in chunk_text(content):
        inputs = tokenizer(chunk, max_length=512, return_tensors="pt", truncation=True)
        inputs = {key: value.to('cuda') for key, value in inputs.items()}
        summary_ids = model.generate(inputs["input_ids"], num_beams=5, max_length=150, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    summarized_text = ' '.join(summaries)
    logger.info("Summarized content: %s", summarized_text)
    return summarized_text
