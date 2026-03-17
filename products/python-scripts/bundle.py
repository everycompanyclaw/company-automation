"""
Python Automation Scripts Bundle
20 Ready-to-Use Scripts for Business Automation
"""

# Script 1: Email Extractor from Text
import re

def extract_emails(text):
    """Extract all emails from any text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

# Usage
# text = "Contact john@email.com or jane@company.org"
# emails = extract_emails(text)
# print(emails)


# Script 2: CSV to JSON Converter
import csv
import json

def csv_to_json(csv_file, json_file):
    """Convert CSV to JSON"""
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    return f"Converted {len(data)} rows"


# Script 3: Screenshot Taker
from datetime import datetime

def take_screenshot(driver, filename=None):
    """Take screenshot with timestamp"""
    if not filename:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    driver.save_screenshot(filename)
    return filename


# Script 4: Google Sheets to CSV
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def sheets_to_csv(sheet_name, credentials_json, output_csv):
    """Download Google Sheet as CSV"""
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    return f"Downloaded {len(data)} rows"


# Script 5: Auto-File Organizer
import os
import shutil
from pathlib import Path

def organize_downloads(download_dir):
    """Organize files by type"""
    extensions = {
        'images': ['.jpg', '.png', '.gif', '.svg'],
        'documents': ['.pdf', '.doc', '.docx', '.txt'],
        'spreadsheets': ['.xlsx', '.csv', '.xls'],
        'code': ['.py', '.js', '.html', '.css'],
        'archives': ['.zip', '.rar', '.7z']
    }
    
    for file in Path(download_dir).iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            for folder, exts in extensions.items():
                if ext in exts:
                    dest = Path(download_dir) / folder
                    dest.mkdir(exist_ok=True)
                    shutil.move(str(file), str(dest))
                    break


# Script 6: URL Status Checker
import requests

def check_urls(urls):
    """Check if URLs are alive"""
    results = []
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            results.append({
                'url': url,
                'status': r.status_code,
                'alive': r.status_code == 200
            })
        except:
            results.append({'url': url, 'status': 'error', 'alive': False})
    return results


# Script 7: Image Resizer
from PIL import Image

def resize_image(input_path, output_path, width=None, height=None):
    """Resize image maintaining aspect ratio"""
    img = Image.open(input_path)
    
    if width and not height:
        height = int(img.height * (width / img.width))
    elif height and not width:
        width = int(img.width * (height / img.height))
    
    img = img.resize((width, height), Image.LANCZOS)
    img.save(output_path)
    return f"Resized to {width}x{height}"


# Script 8: PDF Page Extractor
from PyPDF2 import PdfReader, PdfWriter

def extract_pages(input_pdf, output_pdf, pages):
    """Extract specific pages from PDF"""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    for page_num in pages:
        writer.add_page(reader.pages[page_num - 1])  # 0-indexed
    
    with open(output_pdf, 'wb') as f:
        writer.write(f)
    
    return f"Extracted {len(pages)} pages"


# Script 9: Word Count Analyzer
from collections import Counter

def analyze_text(text):
    """Analyze text for word frequency"""
    words = text.lower().split()
    word_count = Counter(words)
    
    return {
        'total_words': len(words),
        'unique_words': len(word_count),
        'top_10': word_count.most_common(10),
        'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
    }


# Script 10: Date Range Generator
from datetime import datetime, timedelta

def date_range(start_date, end_date):
    """Generate list of dates between start and end"""
    dates = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current <= end:
        dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    
    return dates


# Script 11: Duplicate File Finder
import hashlib

def find_duplicates(directory):
    """Find duplicate files by hash"""
    hashes = {}
    
    for file in Path(directory).rglob('*'):
        if file.is_file():
            with open(file, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in hashes:
                    hashes[file_hash].append(str(file))
                else:
                    hashes[file_hash] = [str(file)]
    
    return {k: v for k, v in hashes.items() if len(v) > 1}


# Script 12: JSON to CSV
def json_to_csv(json_file, csv_file):
    """Convert JSON to CSV"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    if not data:
        return "No data"
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    return f"Converted {len(data)} rows"


# Script 13: Website Metadata Scraper
from bs4 import BeautifulSoup

def scrape_meta(url):
    """Extract metadata from website"""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    return {
        'title': soup.find('title').text if soup.find('title') else '',
        'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else '',
        'og_title': soup.find('meta', property='og:title')['content'] if soup.find('meta', property='og:title'}) else ''
    }


# Script 14: Timer Decorator
import time
from functools import wraps

def timer(func):
    """Decorator to time function execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper


# Script 15: Retry Decorator
from functools import wraps

def retry(max_attempts=3, delay=1):
    """Decorator to retry failed functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


# Script 16: Text to Speech (offline)
from gtts import gTTS

def text_to_speech(text, output_file):
    """Convert text to speech"""
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    return f"Saved to {output_file}"


# Script 17: URL Shortener
def shorten_url(long_url, api_key=None):
    """Shorten URL using TinyURL or custom API"""
    # Using TinyURL (no API key needed)
    r = requests.get(f'https://tinyurl.com/api-create.php?url={long_url}')
    return r.text if r.status_code == 200 else None


# Script 18: Invoice Generator
def generate_invoice(invoice_num, client_name, items, output_file):
    """Generate simple invoice PDF"""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    c = canvas.Canvas(output_file, pagesize=letter)
    c.drawString(100, 750, f"Invoice #{invoice_num}")
    c.drawString(100, 730, f"Client: {client_name}")
    
    y = 700
    total = 0
    for item, price in items:
        c.drawString(100, y, f"{item}: ${price}")
        total += price
        y -= 20
    
    c.drawString(100, y, f"Total: ${total}")
    c.save()
    
    return f"Invoice saved to {output_file}"


# Script 19: Weather Checker
def get_weather(city, api_key):
    """Get current weather"""
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    data = r.json()
    
    return {
        'city': data['name'],
        'temp': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity']
    }


# Script 20: Backup Script
import shutil
from datetime import datetime

def backup_files(source_dir, backup_dir):
    """Create timestamped backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(backup_dir) / f"backup_{timestamp}"
    
    shutil.copytree(source_dir, backup_path)
    return f"Backup created: {backup_path}"
