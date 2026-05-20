# COMP3011 Search Engine Tool

Python command-line search engine tool for COMP3011 Web Services and Web Data coursework.

The tool crawls `https://quotes.toscrape.com/`, builds an inverted index, saves and loads the index, and allows users to search indexed pages.

---

# Features

- Crawls all quote pages from the target website
- Respects a 6-second politeness delay between requests
- Extracts quote text, authors, and tags
- Builds an inverted index with:
  - word frequency
  - word positions
  - page URLs
- Supports case-insensitive search
- Supports ranked multi-word queries
- Saves and loads index from JSON
- Includes automated tests with pytest

---

# Project Structure

```text
src/
  crawler.py
  indexer.py
  storage.py
  search.py
  main.py

tests/
  test_crawler.py
  test_indexer.py
  test_search.py
  test_storage.py
  test_integration.py

data/
  index.json
```

---

# Installation

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment (Windows PowerShell):

```bash
.\venv\Scripts\Activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Tool

```bash
python -m src.main
```

---

# Available Commands

## Build index

```text
build
```

Crawls the website, builds the inverted index, and saves it to:

```text
data/index.json
```

---

## Load index

```text
load
```

Loads the previously saved index from disk.

---

## Print word entry

```text
print life
```

Displays the inverted index entry for a word, including:

- page URLs
- frequency
- word positions

---

## Find pages

```text
find life love
```

Returns pages containing all query words, ranked by combined frequency score.

---

## Edge Cases

```text
find nonsenseword
find
print
```

The tool handles:

- missing words
- empty queries
- invalid input
- missing index files

gracefully with user-friendly error messages.

---

# Testing

Run all tests:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

The test suite includes:

- crawler tests with mocked HTML pages
- indexer unit tests
- search functionality tests
- storage tests
- integration workflow tests

---

# Design Decisions

The project uses a modular architecture:

- `crawler.py` handles web crawling and content extraction
- `indexer.py` builds the inverted index
- `storage.py` saves and loads the index
- `search.py` handles query processing and ranking
- `main.py` provides the command-line interface

Search results are ranked using total query-term frequency across matching pages.

The crawler extracts:

- quote text
- author names
- tags

to reduce irrelevant page noise during indexing.

---

# Technologies Used

- Python 3.11
- Requests
- BeautifulSoup4
- Pytest
- Pytest-Cov

---

# GenAI Use

Generative AI tools were used during development for architectural planning, implementation support, debugging assistance, code review, and improving automated testing.

AI assistance was particularly useful when developing the crawler workflow, refining the inverted index structure, improving query-processing logic, and identifying additional edge cases for testing.

However, all generated suggestions were critically evaluated, manually tested, modified where necessary, and fully understood before integration into the final implementation.

Overall, Generative AI accelerated development and testing workflows while still requiring manual debugging, validation, and software engineering decisions throughout the project.

A full critical reflection on GenAI use is included in the video demonstration.
