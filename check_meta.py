"""
Meta Tag Checker Script
Extracts meta titles and descriptions from web pages listed in a CSV file.

Usage:
    1. Edit config.py to set your BASE_URL, INPUT_FILE, and OUTPUT_FILE
    2. Run: python3 check_meta.py
"""

import csv
import urllib.request
import urllib.error
from html.parser import HTMLParser
import time
import sys

# Import configuration from external file
try:
    from config import BASE_URL, INPUT_FILE, OUTPUT_FILE, DELAY_SECONDS, REQUEST_TIMEOUT
except ImportError:
    print("Error: config.py file not found!")
    print("Please create a config.py file with the required settings.")
    print("See config.py.example for reference.")
    sys.exit(1)

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_description = None
        self.title = None
        self.found_description = False
        self.in_title = False
        self.title_content = []

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            attrs_dict = dict(attrs)
            # Check for name="description"
            if attrs_dict.get('name', '').lower() == 'description':
                self.meta_description = attrs_dict.get('content', '')
                self.found_description = True
        elif tag == 'title':
            self.in_title = True
            self.title_content = []
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
            self.title = ''.join(self.title_content)
    
    def handle_data(self, data):
        if self.in_title:
            self.title_content.append(data)

def check_url(url):
    """
    Check a URL and extract meta title and description.
    
    Args:
        url: Full URL to check
        
    Returns:
        Tuple of (status, description, title)
    """
    try:
        # User-Agent and other headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': BASE_URL + '/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            if response.status != 200:
                return f"Error: Status {response.status}", None, None
            
            html_content = response.read().decode('utf-8', errors='ignore')
            
            parser = MetaParser()
            parser.feed(html_content)
            
            status = "Found" if parser.found_description else "Not Found"
            return status, parser.meta_description, parser.title
                
    except urllib.error.HTTPError as e:
        return f"HTTP Error: {e.code}", None, None
    except urllib.error.URLError as e:
        return f"URL Error: {e.reason}", None, None
    except Exception as e:
        return f"Error: {str(e)}", None, None

def main():
    print(f"Reading from {INPUT_FILE}...")
    
    results = []
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            paths = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Found {len(paths)} pages to check.")
    print(f"Writing results to {OUTPUT_FILE}...")

    # Write header to output file immediately
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'Status', 'Meta Title', 'Meta Description Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, path in enumerate(paths):
            # Ensure path starts with / if not present (though file seems to have them)
            if not path.startswith('/'):
                path = '/' + path
            
            full_url = BASE_URL + path
            print(f"[{i+1}/{len(paths)}] Checking {full_url} ...", end=' ', flush=True)
            
            status, description, title = check_url(full_url)
            
            print(f"-> {status}")
            
            writer.writerow({
                'URL': full_url,
                'Status': status,
                'Meta Title': title if title else '',
                'Meta Description Content': description if description else ''
            })
            
            time.sleep(DELAY_SECONDS)

    print("Done!")

if __name__ == "__main__":
    main()
