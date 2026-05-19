import re


class SearchEngine:
    """
    Handles search operations on the inverted index.
    """

    def __init__(self, index):
        self.index = index

    def _tokenize_query(self, query):
        """
        Normalize a user query into lowercase searchable tokens.
        Removes punctuation and extra spaces.
        """
        return re.findall(r"\b[a-zA-Z0-9']+\b", query.lower())

    def print_word(self, word):
        """
        Return inverted index entry for a single word.
        """
        tokens = self._tokenize_query(word)

        if len(tokens) != 1:
            return None

        return self.index.get(tokens[0])

    def find_query(self, query):
        """
        Find pages containing all query terms.
        Results are ranked by total term frequency.
        """
        query_words = self._tokenize_query(query)

        if not query_words:
            return []

        unique_query_words = list(dict.fromkeys(query_words))

        page_sets = []

        for word in unique_query_words:
            if word not in self.index:
                return []

            page_sets.append(set(self.index[word].keys()))

        matching_pages = set.intersection(*page_sets)

        ranked_results = []

        for page in matching_pages:
            total_score = sum(
                self.index[word][page]["frequency"]
                for word in unique_query_words
            )

            ranked_results.append(
                {
                    "url": page,
                    "score": total_score
                }
            )

        ranked_results.sort(
            key=lambda result: (-result["score"], result["url"])
        )

        return ranked_results