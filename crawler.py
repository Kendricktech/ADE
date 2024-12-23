import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd

class SiteCrawler:
    def __init__(self, base_url, log_file='crawl_logs.csv'):
        self.base_url = base_url
        self.visited_urls = set()
        self.log_file = log_file
        self.init_csv()

    def init_csv(self):
        """Initializes the CSV file with headers."""
        df = pd.DataFrame(columns=['URL', 'Status'])
        df.to_csv(self.log_file, index=False)

    def crawl(self, url):
        """Recursively crawls the site starting from the given URL."""
        if url in self.visited_urls or not self.is_internal_url(url):
            return

        self.visited_urls.add(url)
        try:
            response = requests.get(url, timeout=10)
            status = response.status_code
            print(f"Visited: {url} (Status: {status})")
            self.log_status(url, status)
            if status < 400:  # Continue crawling only for non-error responses
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in self.extract_links(soup, url):
                    self.crawl(link)
        except requests.RequestException as e:
            print(f"Error visiting {url}: {str(e)}")
            self.log_status(url, "Error")

    def extract_links(self, soup, current_url):
        """Extracts and normalizes all links from the page."""
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = urljoin(current_url, a_tag['href'])
            # Normalize and filter
            if self.is_internal_url(href):
                links.add(href)
        return links

    def is_internal_url(self, url):
        """Checks if the URL belongs to the same domain as the base URL."""
        base_netloc = urlparse(self.base_url).netloc
        url_netloc = urlparse(url).netloc
        return base_netloc == url_netloc

    def log_status(self, url, status):
        """Logs the URL and its status code to the CSV file."""
        df = pd.DataFrame([{'URL': url, 'Status': status}])
        df.to_csv(self.log_file, mode='a', header=False, index=False)

# Usage
if __name__ == "__main__":
    base_url = "http://localhost:8000"  # Replace with your site's base URL
    crawler = SiteCrawler(base_url)
    crawler.crawl(base_url)
