import time
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"
REQUEST_DELAY = 6


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class WebCrawler:
    """
    Crawls quotes.toscrape.com and extracts page text.
    """

    def __init__(self, base_url=BASE_URL, delay=REQUEST_DELAY):
        self.base_url = base_url
        self.delay = delay
        self.visited_urls = set()

    def fetch_page(self, url):
        """
        Fetch HTML content from a URL.
        """

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            logging.info(f"Successfully fetched: {url}")

            return response.text

        except requests.RequestException as error:
            logging.error(f"Request failed for {url}: {error}")
            return None

    def extract_page_text(self, html):
        """
        Extract clean text from HTML.
        """

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        return text

    def get_next_page(self, html, current_url):
        """
        Find next page URL from pagination.
        """

        soup = BeautifulSoup(html, "html.parser")

        next_button = soup.select_one("li.next a")

        if next_button:
            next_href = next_button.get("href")
            return urljoin(current_url, next_href)

        return None

    def crawl(self):
        """
        Crawl all pages starting from base URL.
        """

        current_url = self.base_url
        crawled_pages = {}

        while current_url:

            if current_url in self.visited_urls:
                break

            logging.info(f"Crawling page: {current_url}")

            html = self.fetch_page(current_url)

            if html is None:
                break

            page_text = self.extract_page_text(html)

            crawled_pages[current_url] = page_text

            self.visited_urls.add(current_url)

            next_page = self.get_next_page(html, current_url)

            if next_page:
                logging.info(
                    f"Waiting {self.delay} seconds before next request..."
                )
                time.sleep(self.delay)

            current_url = next_page

        logging.info(
            f"Finished crawling {len(crawled_pages)} pages."
        )

        return crawled_pages