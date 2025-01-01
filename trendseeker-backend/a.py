import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import logging
import time
import signal
import sys

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['news_database']
collection = db['headlines']

# Logging setup
logging.basicConfig(level=logging.INFO)

# Function to fetch and store data
def fetch_and_store():
    scrape_toi()
    scrape_the_hindu()
    scrape_indian_express()
    scrape_ndtv()
    scrape_india_today()

# Define scraping functions for different news sources
def scrape_toi():
    url = 'https://timesofindia.indiatimes.com'
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []
    
    for item in soup.select('figcaption'):
        headline_text = item.get_text().strip()
        link = item.find_parent('a')['href'] if item.find_parent('a') else ''
        if headline_text and link:
            if not collection.find_one({'headline': headline_text, 'source': 'TOI'}):
                headlines.append({
                    'headline': headline_text,
                    'link': url + link,
                    'source': 'TOI',
                    'timestamp': datetime.now()
                })
    
    if headlines:
        collection.insert_many(headlines)
        logging.info(f"Inserted {len(headlines)} headlines into MongoDB from TOI.")
    else:
        logging.warning("No new headlines found for TOI")

def scrape_the_hindu():
    url = 'https://www.thehindu.com'
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for item in soup.select('a'):
        if item.get('href') and item.text.strip():
            if not collection.find_one({'headline': item.text.strip(), 'source': 'The Hindu'}):
                headlines.append({
                    'headline': item.text.strip(),
                    'link': item.get('href'),
                    'source': 'The Hindu',
                    'timestamp': datetime.now()
                })

    if headlines:
        collection.insert_many(headlines)
        logging.info(f"Inserted {len(headlines)} headlines into MongoDB from The Hindu.")
    else:
        logging.warning("No new headlines found for The Hindu")

def scrape_indian_express():
    url = 'https://indianexpress.com'
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for item in soup.select('a'):
        if item.get('href') and item.text.strip():
            if not collection.find_one({'headline': item.text.strip(), 'source': 'Indian Express'}):
                headlines.append({
                    'headline': item.text.strip(),
                    'link': item.get('href'),
                    'source': 'Indian Express',
                    'timestamp': datetime.now()
                })

    if headlines:
        collection.insert_many(headlines)
        logging.info(f"Inserted {len(headlines)} headlines into MongoDB from Indian Express.")
    else:
        logging.warning("No new headlines found for Indian Express")

def scrape_ndtv():
    url = 'https://www.ndtv.com'
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for item in soup.select('a'):
        if item.get('href') and item.text.strip():
            if not collection.find_one({'headline': item.text.strip(), 'source': 'NDTV'}):
                headlines.append({
                    'headline': item.text.strip(),
                    'link': item.get('href'),
                    'source': 'NDTV',
                    'timestamp': datetime.now()
                })

    if headlines:
        collection.insert_many(headlines)
        logging.info(f"Inserted {len(headlines)} headlines into MongoDB from NDTV.")
    else:
        logging.warning("No new headlines found for NDTV")

def scrape_india_today():
    url = 'https://www.indiatoday.in'
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for item in soup.select('a'):
        if item.get('href') and item.text.strip():
            if not collection.find_one({'headline': item.text.strip(), 'source': 'India Today'}):
                headlines.append({
                    'headline': item.text.strip(),
                    'link': item.get('href'),
                    'source': 'India Today',
                    'timestamp': datetime.now()
                })

    if headlines:
        collection.insert_many(headlines)
        logging.info(f"Inserted {len(headlines)} headlines into MongoDB from India Today.")
    else:
        logging.warning("No new headlines found for India Today")

# Signal handler to stop the script gracefully
def signal_handler(sig, frame):
    print('Stopping the scraper...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    while True:
        
        fetch_and_store()

        time.sleep(10)

        
