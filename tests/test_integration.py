from src.indexer import InvertedIndexer
from src.search import SearchEngine
from src.storage import IndexStorage


def test_full_index_and_search_workflow(tmp_path):
    pages = {
        "page1": "life love happiness",
        "page2": "life success",
        "page3": "love inspiration"
    }

    indexer = InvertedIndexer()

    index = indexer.build_index(pages)

    filepath = tmp_path / "integration_index.json"

    storage = IndexStorage(filepath)

    storage.save_index(index)

    loaded_index = storage.load_index()

    search_engine = SearchEngine(loaded_index)

    results = search_engine.find_query("life love")

    assert len(results) == 1
    assert results[0]["url"] == "page1"


def test_saved_index_matches_original_index(tmp_path):
    pages = {
        "page1": "life life love"
    }

    indexer = InvertedIndexer()

    original_index = indexer.build_index(pages)

    filepath = tmp_path / "saved_index.json"

    storage = IndexStorage(filepath)

    storage.save_index(original_index)

    loaded_index = storage.load_index()

    assert loaded_index == original_index


def test_search_after_loading_index(tmp_path):
    pages = {
        "page1": "success motivation",
        "page2": "motivation life"
    }

    indexer = InvertedIndexer()

    index = indexer.build_index(pages)

    filepath = tmp_path / "workflow_index.json"

    storage = IndexStorage(filepath)

    storage.save_index(index)

    loaded_index = storage.load_index()

    search_engine = SearchEngine(loaded_index)

    results = search_engine.find_query("motivation")

    assert len(results) == 2