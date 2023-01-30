from skillner.matchers.sliding_window import SlidingWindowMatcher


def test_combine_filters():
    # lowered and then remove num and two char words from text
    text_to_filter = (
        "Born in summer 2021 SkillNER is THE next 2nd Gen of skill extractors"
    )

    combined_filters = SlidingWindowMatcher.combine_filters(
        filters=[
            # lowercase_word
            lambda word: word.lower(),
            # filter_numbers
            lambda word: word if word.isalpha() else None,
            # filter_two_char
            lambda word: None if word in ("in", "is", "of") else word,
        ]
    )

    # the built query for the KG
    filtered_text = " ".join(
        filter(
            None,
            (combined_filters(word) for word in text_to_filter.split()),
        )
    )

    assert filtered_text == "born summer skillner the next gen skill extractors"


if __name__ == "__main__":
    pass
