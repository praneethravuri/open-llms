import requests
import json
import nltk
import regex as re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

def search_question(query):
    url = "http://localhost:8080"
    params = {
        'q': query,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error making request: {response.status_code}")
        return {}
    
    results = response.json()
    return results

def preprocess_text(text):
    # Remove unicode characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Tokenize the text
    words = word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    # Join the words back into a single string
    cleaned_text = ' '.join(filtered_words)
    
    return cleaned_text

def fetch_web_content(question):
    results = search_question(query=question).get("results", [])
    
    context = [preprocess_text(curr_result["content"]) for curr_result in results]
    return context
