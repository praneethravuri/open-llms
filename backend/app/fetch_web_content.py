import requests
import json
import nltk
import regex as re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from requests.exceptions import RequestException, ConnectionError, Timeout, HTTPError

# Ensure NLTK data is downloaded
nltk.download('punkt_tab')
nltk.download('stopwords')

def search_question(query):
    url = "http://localhost:8080"
    params = {
        'q': query,
        'format': 'json'
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params, timeout=10)
        
        # Raise an exception for HTTP errors (4xx/5xx)
        response.raise_for_status()
        
    except ConnectionError:
        print("Error: Unable to connect to the server. Please check the server or your connection.")
        return {}
    except Timeout:
        print("Error: The request timed out.")
        return {}
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {}
    except RequestException as req_err:
        print(f"Error making request: {req_err}")
        return {}

    # Handle potential invalid JSON responses
    try:
        results = response.json()
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON from the response.")
        return {}

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
    
    if not results:
        print("No results found for the question.")
        return []
    
    context = []
    for curr_result in results:
        # Check for content, fallback to 'snippet' or 'title' if needed
        content = curr_result.get("content") or curr_result.get("snippet") or curr_result.get("title")
        if content:
            context.append(preprocess_text(content))
        else:
            print("No usable content in result:", curr_result)

    return context
