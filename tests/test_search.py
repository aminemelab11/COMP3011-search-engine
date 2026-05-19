from src.search import SearchEngine


SAMPLE_INDEX = {
    "life": {
        "page1": {"frequency": 3, "positions": [1, 5, 9]},
        "page2": {"frequency": 1, "positions": [4]},
        "page3": {"frequency": 2, "positions": [2, 6]},
    },
    "love": {
        "page1": {"frequency": 2, "positions": [2, 8]},
        "page3": {"frequency": 1, "positions": [7]},
    },
    "success": {
        "page2": {"frequency": 5, "positions": [1, 2, 3, 4, 5]},
    },
}


def test_print_word_existing_word_returns_index_entry():
    search_engine = SearchEngine(SAMPLE_INDEX)

    result = search_engine.print_word("life")

    assert result is not None
    assert "page1" in result
    assert result["page1"]["frequency"] == 3
    assert result["page1"]["positions"] == [1, 5, 9]


def test_print_word_is_case_insensitive():
    search_engine = SearchEngine(SAMPLE_INDEX)

    result = search_engine.print_word("LIFE")

    assert result == SAMPLE_INDEX["life"]


def test_print_word_handles_punctuation():
    search_engine = SearchEngine(SAMPLE_INDEX)

    result = search_engine.print_word("life!")

    assert result == SAMPLE_INDEX["life"]


def test_print_word_missing_word_returns_none():
    search_engine = SearchEngine(SAMPLE_INDEX)

    result = search_engine.print_word("unknown")

    assert result is None


def test_print_word_rejects_multiple_words():
    search_engine = SearchEngine(SAMPLE_INDEX)

    result = search_engine.print_word("life love")

    assert result is None


def test_find_query_single_word_returns_all_matching_pages_ranked():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("life")

    assert len(results) == 3
    assert results[0]["url"] == "page1"
    assert results[0]["score"] == 3
    assert results[1]["url"] == "page3"
    assert results[1]["score"] == 2
    assert results[2]["url"] == "page2"
    assert results[2]["score"] == 1


def test_find_query_multiple_words_returns_intersection_only():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("life love")

    assert len(results) == 2
    assert results[0]["url"] == "page1"
    assert results[1]["url"] == "page3"


def test_find_query_multiple_words_are_ranked_by_combined_score():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("life love")

    assert results[0]["url"] == "page1"
    assert results[0]["score"] == 5
    assert results[1]["url"] == "page3"
    assert results[1]["score"] == 3


def test_find_query_is_case_insensitive():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("LIFE LOVE")

    assert len(results) == 2


def test_find_query_handles_extra_spaces():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("   life     love   ")

    assert len(results) == 2


def test_find_query_handles_punctuation():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("life, love!")

    assert len(results) == 2


def test_find_query_repeated_words_do_not_double_count_score():
    search_engine = SearchEngine(SAMPLE_INDEX)

    normal_results = search_engine.find_query("life love")
    repeated_results = search_engine.find_query("life life love")

    assert repeated_results == normal_results


def test_find_query_unknown_word_returns_empty_list():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("unknown")

    assert results == []


def test_find_query_partially_missing_query_returns_empty_list():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("life unknown")

    assert results == []


def test_find_query_empty_string_returns_empty_list():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("")

    assert results == []


def test_find_query_only_punctuation_returns_empty_list():
    search_engine = SearchEngine(SAMPLE_INDEX)

    results = search_engine.find_query("!!! ???")

    assert results == []