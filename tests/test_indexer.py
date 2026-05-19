from src.indexer import InvertedIndexer


def test_tokenize_lowercase():
    indexer = InvertedIndexer()
    tokens = indexer.tokenize("Life LOVE Success")

    assert "life" in tokens
    assert "love" in tokens
    assert "success" in tokens


def test_tokenize_removes_stop_words():
    indexer = InvertedIndexer()
    tokens = indexer.tokenize("The life and love of success")

    assert "the" not in tokens
    assert "and" not in tokens
    assert "of" not in tokens
    assert "life" in tokens
    assert "love" in tokens


def test_build_index_frequency_and_positions():
    indexer = InvertedIndexer()

    pages = {
        "page1": "life love life",
        "page2": "love success"
    }

    index = indexer.build_index(pages)

    assert index["life"]["page1"]["frequency"] == 2
    assert index["life"]["page1"]["positions"] == [0, 2]

    assert index["love"]["page1"]["frequency"] == 1
    assert index["love"]["page2"]["frequency"] == 1