import requests
from bs4 import BeautifulSoup
from googlesearch import search
import logging

logger = logging.getLogger(__name__)

def fetch_text(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, cookies={'CONSENT':'YES+'})
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        logger.info("Fetched content from %s", url)
        return content
    except Exception as e:
        logger.error("Error fetching content from %s: %s", url, e)
        return ""

def fetch_web_content(query):
    response = []
    search_results = search(query, num_results=10)
    for url in search_results:
        content = fetch_text(url)
        if content:
            paragraphs = content.split("\n")
            response.extend(paragraphs)
    logger.info("Fetched web content for query: %s", query)
    return response

def process_query(query):
    web_content = fetch_web_content(query)
    # You can integrate this with your LLM processing here
    processed_content = " ".join(web_content[:5])  # Limit the output for simplicity
    return processed_content
