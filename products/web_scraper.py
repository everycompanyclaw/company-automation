#!/usr/bin/env python3
"""Web Scraper Pro - Scrape any website"""
import requests
from bs4 import BeautifulSoup

def scrape(url, selector):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return [elem.text for elem in soup.select(selector)]

if __name__ == "__main__":
    # Example: scrape quotes
    quotes = scrape("http://quotes.toscrape.com", ".quote span.text")
    for q in quotes:
        print(q)
