from src.crawler import WebCrawler
from src.indexer import InvertedIndexer
from src.search import SearchEngine


crawler = WebCrawler()

pages = crawler.crawl()

indexer = InvertedIndexer()

index = indexer.build_index(pages)

search_engine = SearchEngine(index)


print("\n===== PRINT WORD TEST =====")

word_result = search_engine.print_word("life")

print(word_result)


print("\n===== FIND QUERY TEST =====")

query_result = search_engine.find_query("life love")

for result in query_result:
    print(result)