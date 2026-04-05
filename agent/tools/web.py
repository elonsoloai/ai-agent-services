"""
Example: Web Scraping Tool
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, List

class WebTool:
    """Simple web scraping tool"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AI-Agent/1.0)'
        })

    def fetch(self, url: str) -> Optional[str]:
        """Fetch page content"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_text(self, html: str) -> str:
        """Extract clean text from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        # Remove scripts and styles
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        return soup.get_text(separator='\n', strip=True)

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from page"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                links.append(base_url.rstrip('/') + href)
        return list(set(links))


if __name__ == "__main__":
    tool = WebTool()

    # Demo: fetch a page
    html = tool.fetch("https://example.com")
    if html:
        text = tool.extract_text(html)
        print(f"Content length: {len(text)} chars")
        print(f"Preview:\n{text[:500]}...")
