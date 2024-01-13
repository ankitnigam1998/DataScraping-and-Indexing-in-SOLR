import wikipedia
import pysolr
import re

# Define the Solr core name and VM IP
CORE_NAME = "sample_test"
VM_IP = "104.154.196.16"

class Indexer:
    def __init__(self):
        self.solr_url = f'https://{VM_IP}:8983/solr/'
        self.connection = pysolr.Solr(f"http://{VM_IP}:8983/solr/" + CORE_NAME, always_commit = True, timeout = 10000)

    def create_documents(self, docs):
        print(self.connection.add(docs))

def clean_summary(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text

import time

def scrape_wikipedia(topic, min_unique_documents=500, min_summary_length=200):
    documents = []
    search_results = wikipedia.search(topic, results=min_unique_documents)
    for page_title in search_results:
        try:
            page = wikipedia.page(page_title)
            if len(page.summary) >= min_summary_length:
                cleaned_summary = clean_summary(page.summary)
                if cleaned_summary:
                    document = {
                        "revision_id": page.revision_id,
                        "title": page.title,
                        "summary": cleaned_summary,
                        "url": page.url,
                        "topic": topic,
                    }
                    documents.append(document)
                    print(f"Scraped {len(documents)} documents for {topic}: {page.title}...")
            time.sleep(1)
        except wikipedia.exceptions.PageError as e:
            pass
        except wikipedia.exceptions.DisambiguationError as e:
            pass

    return documents

topics = ["Health", "Environment", "Technology", "Economy", "Entertainment", "Sports", "Politics", "Education", "Travel", "Food"]

indexer = Indexer()

for topic in topics:
    print(f"Scraping data for {topic}...")
    scraped_data = scrape_wikipedia(topic, min_unique_documents = 700)
    print(f"Indexing {len(scraped_data)} documents for {topic} in Solr...")
    indexer.create_documents(scraped_data)

import pysolr

CORE_NAME = "IRF23P1"
VM_IP = "104.154.196.16"

solr = pysolr.Solr(f"http://{VM_IP}:8983/solr/{CORE_NAME}", always_commit=True, timeout=10000)

query = "*:*"

results = solr.search(query)

print(f"Total documents found: {results.hits}")

for result in results:
    print("Document:")
    print(f"  Revision ID: {result['revision_id']}")
    print(f"  Title: {result['title']}")
    print(f"  Summary: {result['summary']}")
    print(f"  URL: {result['url']}")
    print(f"  Topic: {result['topic']}")
    print("\n")

import pysolr
import json

CORE_NAME = "sample_test"
VM_IP = "104.154.196.16"

solr = pysolr.Solr(f"http://{VM_IP}:8983/solr/{CORE_NAME}", always_commit=True, timeout=100000)

start = 0
rows = 100

documents = []

while True:

    query = "*:*"

    results = solr.search(query, start=start, rows=rows)

    for result in results:
        document = {
            "revision_id": result['revision_id'],
            "title": result['title'],
            "summary": result['summary'],
            "url": result['url'],
            "topic": result['topic']
        }
        documents.append(document)

    if len(results) < rows:
        break

    start += rows

json_file_path = "indexed_documents.json"

with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(documents, json_file, ensure_ascii=False, indent=4)

print(f"Indexed documents saved to {json_file_path}")

