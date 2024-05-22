import requests
from bs4 import BeautifulSoup
from googlesearch import search

def fetch_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

def fetch_web_content(query):
    response = []
    search_results = search(query, num_results=5)
    for url in search_results:
        content = fetch_text(url)
        if content:
            paragraphs = content.split("\n")
            response.extend(paragraphs)
    return response
