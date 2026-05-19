import os
import pytest

from src.storage import IndexStorage


SAMPLE_INDEX = {
    "life": {
        "page1": {
            "frequency": 2,
            "positions": [1, 5]
        }
    }
}


def test_save_index_creates_file(tmp_path):
    filepath = tmp_path / "test_index.json"

    storage = IndexStorage(filepath)

    storage.save_index(SAMPLE_INDEX)

    assert os.path.exists(filepath)


def test_load_index_returns_saved_data(tmp_path):
    filepath = tmp_path / "test_index.json"

    storage = IndexStorage(filepath)

    storage.save_index(SAMPLE_INDEX)

    loaded_index = storage.load_index()

    assert loaded_index == SAMPLE_INDEX


def test_load_index_raises_file_not_found_error(tmp_path):
    filepath = tmp_path / "missing_index.json"

    storage = IndexStorage(filepath)

    with pytest.raises(FileNotFoundError):
        storage.load_index()


def test_save_index_overwrites_existing_file(tmp_path):
    filepath = tmp_path / "test_index.json"

    storage = IndexStorage(filepath)

    first_index = {
        "life": {
            "page1": {
                "frequency": 1,
                "positions": [0]
            }
        }
    }

    second_index = {
        "love": {
            "page2": {
                "frequency": 3,
                "positions": [1, 2, 3]
            }
        }
    }

    storage.save_index(first_index)
    storage.save_index(second_index)

    loaded_index = storage.load_index()

    assert loaded_index == second_index


def test_save_index_handles_empty_index(tmp_path):
    filepath = tmp_path / "empty_index.json"

    storage = IndexStorage(filepath)

    storage.save_index({})

    loaded_index = storage.load_index()

    assert loaded_index == {}