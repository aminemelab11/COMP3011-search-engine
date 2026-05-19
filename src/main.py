from src.crawler import WebCrawler
from src.indexer import InvertedIndexer
from src.storage import IndexStorage
from src.search import SearchEngine


def display_help():
    print("\nAvailable commands:")
    print("  build              Crawl website, build index, and save it")
    print("  load               Load saved index from file")
    print("  print <word>       Print inverted index entry for a word")
    print("  find <query>       Find pages containing query words")
    print("  help               Show available commands")
    print("  exit               Exit the program\n")


def build_command():
    print("\nBuilding index. This may take around 1 minute due to politeness delay.\n")

    crawler = WebCrawler()
    pages = crawler.crawl()

    indexer = InvertedIndexer()
    index = indexer.build_index(pages)

    storage = IndexStorage()
    saved_path = storage.save_index(index)

    print(f"\nIndex built successfully.")
    print(f"Pages crawled: {len(pages)}")
    print(f"Unique words indexed: {len(index)}")
    print(f"Index saved to: {saved_path}\n")

    return index


def load_command():
    storage = IndexStorage()
    index = storage.load_index()

    print("\nIndex loaded successfully.")
    print(f"Unique words loaded: {len(index)}\n")

    return index


def print_command(search_engine, command):
    parts = command.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        print("Error: please provide a word. Example: print life")
        return

    word = parts[1].strip()
    result = search_engine.print_word(word)

    if result is None:
        print(f"No index entry found for '{word}'.")
        return

    print(f"\nInverted index for '{word.lower()}':")

    for url, stats in result.items():
        print(f"\nURL: {url}")
        print(f"Frequency: {stats['frequency']}")
        print(f"Positions: {stats['positions']}")


def find_command(search_engine, command):
    parts = command.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        print("Error: empty query. Example: find life love")
        return

    query = parts[1].strip()
    results = search_engine.find_query(query)

    if not results:
        print(f"No pages found for query: '{query}'")
        return

    print(f"\nSearch results for '{query}':")

    for result in results:
        print(f"{result['url']} | score: {result['score']}")


def main():
    index = None

    print("COMP3011 Search Engine Tool")
    display_help()

    while True:
        command = input("> ").strip()

        if not command:
            print("Please enter a command. Type 'help' for options.")
            continue

        if command == "exit":
            print("Goodbye.")
            break

        elif command == "help":
            display_help()

        elif command == "build":
            index = build_command()

        elif command == "load":
            try:
                index = load_command()
            except FileNotFoundError as error:
                print(f"Error: {error}")
                print("Run 'build' first to create an index.")

        elif command.startswith("print"):
            if index is None:
                print("No index available. Run 'build' or 'load' first.")
                continue

            search_engine = SearchEngine(index)
            print_command(search_engine, command)

        elif command.startswith("find"):
            if index is None:
                print("No index available. Run 'build' or 'load' first.")
                continue

            search_engine = SearchEngine(index)
            find_command(search_engine, command)

        else:
            print("Unknown command. Type 'help' for available commands.")


if __name__ == "__main__":
    main()