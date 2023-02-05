from skillner.core.data_structures import Word, Sentence, Document, Span, Candidate
from skillner.conflict_resolvers.span_processor import SpanProcessor


class TestConflictResolver:
    text = (
        "i was a student now i am an industrial management "
        "engineer graduated from EMINES"
    )

    def test_span_processor(self):
        # given span select the largest candidate

        # create sentence with two spans
        sentence = Sentence()
        sentence.li_words = [Word(w) for w in self.text.split()]

        # create span on `student`
        span_1 = Span()
        span_1.add_candidate(Candidate(window=slice(3, 5), concept_id=0))

        # create span on `industrial management`
        span_2 = Span()
        span_2.add_candidate(Candidate(window=slice(8, 9), concept_id=1))
        span_2.add_candidate(Candidate(window=slice(8, 10), concept_id=2))

        sentence.li_spans = [span_1, span_2]

        # create doc
        doc = Document()
        doc.li_sentences.append(sentence)

        # resolve conflict by selecting candidate with max length
        max_length_resolver = SpanProcessor(
            dict_filters={
                "max_candidate": lambda span: max(span.li_candidates, key=len)
            }
        )
        max_length_resolver(doc)

        # check that spans were enriched and the max_candidate are the one expected
        span_1, span_2 = doc[0].li_spans
        assert hasattr(span_1, "metadata") and hasattr(span_1, "metadata")
        assert span_1.metadata["max_candidate"].concept_id == 0
        assert span_2.metadata["max_candidate"].concept_id == 2


if __name__ == "__main__":
    pass
