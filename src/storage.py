import json
import os


DEFAULT_INDEX_PATH = "data/index.json"


class IndexStorage:
    """
    Handles saving and loading the inverted index.
    """

    def __init__(self, filepath=DEFAULT_INDEX_PATH):
        self.filepath = filepath

    def save_index(self, index):
        """
        Save inverted index to a JSON file.
        """

        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(index, file, indent=2)

        return self.filepath

    def load_index(self):
        """
        Load inverted index from a JSON file.
        """

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                f"Index file not found: {self.filepath}"
            )

        with open(self.filepath, "r", encoding="utf-8") as file:
            index = json.load(file)

        return index