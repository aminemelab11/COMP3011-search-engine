from src.indexer import InvertedIndexer


def test_tokenize_converts_text_to_lowercase_tokens():
    indexer = InvertedIndexer()

    tokens = indexer.tokenize("Life LOVE Success")

    assert tokens == ["life", "love", "success"]


def test_tokenize_removes_stop_words():
    indexer = InvertedIndexer()

    tokens = indexer.tokenize("The life and love of success")

    assert "the" not in tokens
    assert "and" not in tokens
    assert "of" not in tokens
    assert tokens == ["life", "love", "success"]


def test_tokenize_handles_numbers_and_apostrophes():
    indexer = InvertedIndexer()

    tokens = indexer.tokenize("Einstein's 100 ideas")

    assert "einstein's" in tokens
    assert "100" in tokens
    assert "ideas" in tokens


def test_tokenize_removes_punctuation():
    indexer = InvertedIndexer()

    tokens = indexer.tokenize("Life, love! success?")

    assert tokens == ["life", "love", "success"]


def test_build_index_creates_entries_for_each_word():
    indexer = InvertedIndexer()

    pages = {
        "page1": "life love life",
        "page2": "love success"
    }

    index = indexer.build_index(pages)

    assert "life" in index
    assert "love" in index
    assert "success" in index


def test_build_index_tracks_frequency_correctly():
    indexer = InvertedIndexer()

    pages = {
        "page1": "life love life",
        "page2": "love success"
    }

    index = indexer.build_index(pages)

    assert index["life"]["page1"]["frequency"] == 2
    assert index["love"]["page1"]["frequency"] == 1
    assert index["love"]["page2"]["frequency"] == 1


def test_build_index_tracks_positions_correctly():
    indexer = InvertedIndexer()

    pages = {
        "page1": "life love life"
    }

    index = indexer.build_index(pages)

    assert index["life"]["page1"]["positions"] == [0, 2]
    assert index["love"]["page1"]["positions"] == [1]


def test_build_index_is_case_insensitive():
    indexer = InvertedIndexer()

    pages = {
        "page1": "Life LIFE life"
    }

    index = indexer.build_index(pages)

    assert "life" in index
    assert index["life"]["page1"]["frequency"] == 3


def test_build_index_ignores_stop_words():
    indexer = InvertedIndexer()

    pages = {
        "page1": "the and of life"
    }

    index = indexer.build_index(pages)

    assert "the" not in index
    assert "and" not in index
    assert "of" not in index
    assert "life" in index


def test_build_index_handles_empty_page_text():
    indexer = InvertedIndexer()

    pages = {
        "page1": ""
    }

    index = indexer.build_index(pages)

    assert index == {}


def test_build_index_handles_multiple_pages_for_same_word():
    indexer = InvertedIndexer()

    pages = {
        "page1": "life",
        "page2": "life life"
    }

    index = indexer.build_index(pages)

    assert index["life"]["page1"]["frequency"] == 1
    assert index["life"]["page2"]["frequency"] == 2
    assert index["life"]["page1"]["positions"] == [0]
    assert index["life"]["page2"]["positions"] == [0, 1]


def test_get_index_returns_current_index():
    indexer = InvertedIndexer()

    pages = {
        "page1": "life"
    }

    indexer.build_index(pages)
    index = indexer.get_index()

    assert index == {
        "life": {
            "page1": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }