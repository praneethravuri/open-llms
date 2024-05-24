# import requests
# from bs4 import BeautifulSoup
# from googlesearch import search

# def fetch_text(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = soup.find_all('p')
#         content = ' '.join([para.get_text() for para in paragraphs])
#         return content
#     except Exception as e:
#         print(f"Error fetching content from {url}: {e}")
#         return ""

# def fetch_web_content(query):
#     response = []
#     search_results = search(query, num_results=5)
#     for url in search_results:
#         print(f"URL: {url}")
#         content = fetch_text(url)
#         if content:
#             paragraphs = content.split("\n")
#             response.extend(paragraphs)
#     print(f"Fetched web content: {response}")
#     return response

import requests
import requests
import json

# Define the function to perform the search and save results to a file
def search_and_save(query, filename="search_results.json"):
    url = "http://localhost:8080"
    params = {
        'q': query,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error making the request: {response.status_code}")
        return
    
    results = response.json()
    
    # Write the results to a JSON file
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results written to {filename}")
