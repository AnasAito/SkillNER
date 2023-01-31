from functools import reduce
from typing import List, Callable

from skillner.core.base import Node
from skillner.core.data_structures import Document, Span, Candidate


class SlidingWindowMatcher(Node):
    """Sliding Window matcher class.

    A matcher that uses sliding/shrinking window algorithm to find
    spans in sentence.

    Parameters
    ----------
    query_method: Callable[[str], dict]
        A function that takes a string as entry, aka. the query,
        and returns a response as dictionary if the query matches and ``None``
        otherwise.

    max_window_size: int, default 4
        The maximum number of words to consider when constructing the query.

    filters: List of Callable[[str], str]
        A list of functions that take a string as input and return string or None.
        The filters are applied sequentially on the words in the window before
        building the query.

    """

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
        """Find spans in ``doc``.

        Parameters
        ----------
        doc: Document
            The document in which to find spans.

        """
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

        # sanity check
        if idx_word >= len(sentence):
            return Span()

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

            span.add_candidate(candidate)

        return span

    @staticmethod
    def combine_filters(filters: List[Callable[[str], str]]) -> Callable[[str], str]:
        """Combine sequentially ``filters`` into one filter.

        Given ``filters = [filter_1, ..., filter_n]`` as input, combined
        them sequentially into ``filter_n(...filter_1)``.

        Parameters
        ----------
        filters: List[Callable[[str], str]]
            filters to combine sequentially.

        Returns
        -------
        combined_filter: Callable[[str], str]
            Return a function that takes a word as input and outputs
            filter_n(...(filter_1(word))).

        """
        if len(filters) == 0:
            return lambda word: word

        def chain_two_filters(filter_1, filter_2):
            return lambda word: filter_2(filter_1(word))

        combined_filter = reduce(chain_two_filters, filters)
        return combined_filter
