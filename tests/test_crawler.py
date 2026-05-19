from src.crawler import WebCrawler


SAMPLE_HTML = """
<html>
    <body>
        <div class="quote">
            <span class="text">“Life is beautiful.”</span>
            <small class="author">Albert Einstein</small>
            <div class="tags">
                <a class="tag">life</a>
                <a class="tag">inspiration</a>
            </div>
        </div>
        <li class="next">
            <a href="/page/2/">Next</a>
        </li>
    </body>
</html>
"""


def test_extract_page_text_extracts_quote_author_and_tags():
    crawler = WebCrawler(delay=0)

    text = crawler.extract_page_text(SAMPLE_HTML)

    assert "Life is beautiful" in text
    assert "Albert Einstein" in text
    assert "life" in text
    assert "inspiration" in text


def test_get_next_page_returns_absolute_url():
    crawler = WebCrawler(delay=0)

    next_url = crawler.get_next_page(
        SAMPLE_HTML,
        "https://quotes.toscrape.com/"
    )

    assert next_url == "https://quotes.toscrape.com/page/2/"


def test_get_next_page_returns_none_when_no_next_link():
    crawler = WebCrawler(delay=0)

    html_without_next = "<html><body><p>No next page</p></body></html>"

    next_url = crawler.get_next_page(
        html_without_next,
        "https://quotes.toscrape.com/"
    )

    assert next_url is None


def test_crawl_stops_after_single_page_when_no_next_link(monkeypatch):
    crawler = WebCrawler(delay=0)

    html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“Test quote.”</span>
                <small class="author">Test Author</small>
            </div>
        </body>
    </html>
    """

    def mock_fetch_page(url):
        return html

    monkeypatch.setattr(crawler, "fetch_page", mock_fetch_page)

    pages = crawler.crawl()

    assert len(pages) == 1
    assert crawler.base_url in pages
    assert "Test quote" in pages[crawler.base_url]


def test_crawl_follows_next_page(monkeypatch):
    crawler = WebCrawler(delay=0)

    first_page = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“First quote.”</span>
            </div>
            <li class="next">
                <a href="/page/2/">Next</a>
            </li>
        </body>
    </html>
    """

    second_page = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“Second quote.”</span>
            </div>
        </body>
    </html>
    """

    def mock_fetch_page(url):
        if url.endswith("/page/2/"):
            return second_page
        return first_page

    monkeypatch.setattr(crawler, "fetch_page", mock_fetch_page)

    pages = crawler.crawl()

    assert len(pages) == 2
    assert "https://quotes.toscrape.com/" in pages
    assert "https://quotes.toscrape.com/page/2/" in pages