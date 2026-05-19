from src.crawler import WebCrawler
from src.indexer import InvertedIndexer


crawler = WebCrawler()

pages = crawler.crawl()

indexer = InvertedIndexer()

index = indexer.build_index(pages)

print(f"\nTotal indexed words: {len(index)}")

sample_word = "life"

if sample_word in index:
    print(f"\nIndex entry for '{sample_word}':")
    print(index[sample_word])
else:
    print(f"'{sample_word}' not found.")