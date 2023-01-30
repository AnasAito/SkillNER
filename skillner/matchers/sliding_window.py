from functools import reduce
from typing import List, Callable

from skillner.core.base import Node
from skillner.core.data_structures import Document, Span, Candidate


class SlidingWindowMatcher(Node):
    """"""

    def __init__(
        self,
        query_method: Callable[[str], dict],
        max_window_size: int = 4,
        filters: List[Callable[[str], str]] = [],
    ) -> None:
        self.query_method = query_method
        self.max_window_size = max_window_size
        self.combined_filters = SlidingWindowMatcher.combine_filters(filters)

    def enrich_doc(self, doc: Document) -> None:
        """"""
        for sentence in doc:

            for idx_word in range(len(sentence)):

                span = self.find_span(sentence, idx_word)

                # skip empty spans
                if span.is_empty():
                    continue

                sentence.li_spans.append(span)

    def find_span(self, sentence, idx_word) -> Span:
        """"""
        span = Span()

        for window_size in range(self.max_window_size, 0, -1):

            idx_end = idx_word + window_size

            # window within boundaries of sentence
            if idx_end > len(sentence):
                continue

            window = slice(idx_word, idx_end)

            # construct query
            query = " ".join(
                filter(
                    None,
                    (self.combined_filters(str(word)) for word in sentence[window]),
                )
            )

            # ask knowledge graph
            response = self.query_method(query)

            if response is None:
                continue

            # create candidate
            candidate = Candidate(window)
            candidate.metadata = response

            span.li_candidates.append(candidate)

        return span

    @staticmethod
    def combine_filters(filters: List[Callable[[str], str]]):
        """"""

        if len(filters) == 0:
            return lambda word: word

        def chain_two_filters(filter_1, filter_2):
            return lambda word: filter_2(filter_1(word))

        return reduce(chain_two_filters, filters)
