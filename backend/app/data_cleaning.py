from sentence_transformers import util
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w.lower() in stop_words]
    return ' '.join(filtered_text)

def extract_relevant_paragraphs(paragraphs, question, model):
    question_embedding = model.encode(question, convert_to_tensor=True)
    relevant_paragraphs = []

    for para in paragraphs:
        para_embedding = model.encode(para, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(question_embedding, para_embedding)
        if similarity.item() > 0.2:  # Threshold for relevance, can be adjusted
            relevant_paragraphs.append(para)
    
    # Remove stopwords from relevant paragraphs
    relevant_paragraphs = [preprocess_text(para) for para in relevant_paragraphs]
    print(f"Relevant Paragraphs: {relevant_paragraphs}")
    return relevant_paragraphs