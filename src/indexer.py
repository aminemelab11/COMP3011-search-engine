import re
from collections import defaultdict


class InvertedIndexer:
    """
    Builds an inverted index from crawled pages.
    """

    def __init__(self):

        self.index = defaultdict(dict)

        self.stop_words = {
            "a", "an", "the", "and", "or", "of",
            "to", "in", "is", "it", "for", "on",
            "with", "as", "by", "at", "from"
        }

    def tokenize(self, text):
        """
        Convert text into normalized tokens.
        """

        tokens = re.findall(r"\b[a-zA-Z0-9']+\b", text.lower())

        filtered_tokens = [
            token for token in tokens
            if token not in self.stop_words
        ]

        return filtered_tokens

    def build_index(self, pages):
        """
        Build inverted index from crawled pages.
        """

        for url, text in pages.items():

            tokens = self.tokenize(text)

            for position, token in enumerate(tokens):

                if url not in self.index[token]:

                    self.index[token][url] = {
                        "frequency": 0,
                        "positions": []
                    }

                self.index[token][url]["frequency"] += 1

                self.index[token][url]["positions"].append(position)

        return dict(self.index)

    def get_index(self):
        """
        Return complete index.
        """

        return dict(self.index)