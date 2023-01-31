from skillner.core.data_structures import Document, Sentence, Word
from skillner.matchers.sliding_window import SlidingWindowMatcher


def test_combine_filters():
    # lowered and then remove num and two char words from text
    text_to_filter = (
        "Born in summer 2021 SkillNER is THE next 2nd Gen of skill extractors"
    )

    def pre_filter(w: Word):
        lower_w = w.lower()

        if not lower_w.isalpha():
            return False

        if lower_w in ("in", "is", "of"):
            return False

        return lower_w

    # the built query for the KG
    filtered_text = " ".join(
        filter(
            None,
            (pre_filter(word) for word in text_to_filter.split()),
        )
    )

    assert filtered_text == "born summer skillner the next gen skill extractors"


class TestSlidingWindowMatching:
    knowledge_base = {
        "student": {"id": -2, "type": "academic (primary -> high school)"},
        "engineer student": {"id": -1, "type": "academic (college)"},
        "industrial management engineer": {"id": 0, "type": "profession"},
        "industrial management": {"id": 1, "type": "field"},
        "software": {"id": 2, "type": "stuff"},
        "software engineer": {"id": 3, "type": "profession"},
        "software engineer enthusiast": {"id": 4, "type": "hobby"},
        "emines": {"id": 5, "type": "institution"},
    }

    @staticmethod
    def query_meth(s: str):
        return TestSlidingWindowMatching.knowledge_base.get(s, None)

    def test_matcher(self):
        text = (
            "i was a student now i am an industrial management "
            "engineer graduated from EMINES"
        )

        # init doc with one sentence
        sentence = Sentence()
        sentence.li_words = [Word(s) for s in text.split()]

        doc = Document()
        doc.li_sentences.append(sentence)

        # matcher that matches on lowercase strings
        matcher = SlidingWindowMatcher(
            TestSlidingWindowMatching.query_meth,
            max_window_size=4,
            pre_filter=lambda word: word.lower(),
        )

        # match on KN
        matcher.enrich_doc(doc)

        # check three matches
        sentence: Sentence = doc[0]
        assert len(sentence.li_spans) == 3

        # last match must be 'EMINES'
        last_span = sentence.li_spans[-1]
        print(sentence[last_span.window])
        assert " ".join(sentence[last_span.window]) == "EMINES"

        # mid-match must have two candidates
        mid_span = sentence.li_spans[1]
        assert len(mid_span.li_candidates) == 2


if __name__ == "__main__":
    pass
