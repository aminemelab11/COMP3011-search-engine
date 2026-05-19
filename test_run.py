from src.crawler import WebCrawler

crawler = WebCrawler()

pages = crawler.crawl()

print(f"Total pages crawled: {len(pages)}")