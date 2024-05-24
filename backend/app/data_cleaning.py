from sentence_transformers import util
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Remove unicode characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Remove '...' and other similar patterns
    text = re.sub(r'\.{2,}', ' ', text)
    
    # Tokenize the text
    words = word_tokenize(text)
    
    # Join the words back into a single string
    cleaned_text = ' '.join(words)
    
    print(f"Cleaned text: {cleaned_text}")
    
    return cleaned_text


def extract_relevant_paragraphs(paragraphs, question, model):
    question_embedding = model.encode(question, convert_to_tensor=True)
    relevant_paragraphs = []

    for para in paragraphs:
        para_embedding = model.encode(para, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(question_embedding, para_embedding)
        if similarity.item() > 0.4:  # Threshold for relevance, can be adjusted
            relevant_paragraphs.append(para)
    relevant_paragraphs = [preprocess_text(para) for para in relevant_paragraphs]
    print(f"Relevant Paragraphs: {relevant_paragraphs}")
    return relevant_paragraphs
