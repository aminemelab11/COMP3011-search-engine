class SearchEngine:
    """
    Handles search operations on the inverted index.
    """

    def __init__(self, index):
        self.index = index

    def print_word(self, word):
        """
        Return inverted index entry for a single word.
        """

        normalized_word = word.lower()

        if normalized_word not in self.index:
            return None

        return self.index[normalized_word]

    def find_query(self, query):
        """
        Find pages containing all query terms.
        """

        query_words = query.lower().split()

        if not query_words:
            return []

        page_sets = []

        for word in query_words:

            if word not in self.index:
                return []

            page_sets.append(set(self.index[word].keys()))

        matching_pages = set.intersection(*page_sets)

        ranked_results = []

        for page in matching_pages:

            total_score = sum(
                self.index[word][page]["frequency"]
                for word in query_words
            )

            ranked_results.append(
                {
                    "url": page,
                    "score": total_score
                }
            )

        ranked_results.sort(
            key=lambda result: result["score"],
            reverse=True
        )

        return ranked_results