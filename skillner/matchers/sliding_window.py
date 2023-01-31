from typing import Callable

from skillner.core.base import Node
from skillner.core.data_structures import Document, Sentence, Span, Candidate


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

    max_window_size: int, default=4
        The maximum number of words to consider when constructing the query.

    pre_filter: Callable[[Word], str], default=None
        A function that takes a ``Word`` as input and return ``str`` or ``False``.
        The ``pre_filter`` function is applied to every ``Word`` in the window before
        building the query. If set to ``None``, the query is build using the string form
        the words in window.

    """

    def __init__(
        self,
        query_method: Callable[[str], dict],
        max_window_size: int = 4,
        pre_filter: Callable[[str], str] = None,
    ) -> None:
        self.query_method = query_method
        self.max_window_size = max_window_size

        # TODO: validate pre_filter
        self.pre_filter = pre_filter if pre_filter is not None else lambda w: str(w)

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

    def find_span(self, sentence: Sentence, idx_word: int) -> Span:
        """Finds the span in ``sentence`` given starting index of ``Word``.

        Parameters
        ----------
        sentence: Sentence
            Sentence in which to find span.

        idx_word: ind
            The index of the word from which to start finding.

        Return
        ------
        span: Span
            Found span with candidates. Empty span otherwise.

        """
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
                    (self.pre_filter(word) for word in sentence[window]),
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
