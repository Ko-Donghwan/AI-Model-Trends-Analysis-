import requests
import time
from bs4 import BeautifulSoup

class WebScraper:
    """웹 페이지를 가져오는 책임을 가진 클래스"""
    def __init__(self, max_retries: int = 5, delay: int = 5):
        self.max_retries = max_retries
        self.delay = delay
    def get_page_content(self, url: str) -> BeautifulSoup:
        """웹 페이지를 가져와서 BeautifulSoup 객체로 반환"""
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except (requests.RequestException, requests.Timeout) as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(self.delay)