from typing import Dict, Callable, Any

from skillner.core.base import Node
from skillner.core.data_structures import Document, Span


class SpanProcessor(Node):
    """Span processor class that runs functions on all words of document.

    ``SpanProcessor`` class acts on individual spans of document. It runs
    independently functions and stores the result on the ``metadata``
    dictionary of span.

    Parameters
    ----------
    dict_filters: Dict[str, Callable[[Span], str]]
        A dictionary of functions that take ``Span`` as input.

    """

    def __init__(self, dict_filters: Dict[str, Callable[[Span], Any]]) -> None:
        # TODO: validate dict_filters
        self.dict_filters = dict_filters

    def enrich_doc(self, doc: Document) -> None:
        """Enrich every span of ``doc``.

        Parameters
        ----------
        doc: Document
            The document with spans to be enriched.

        """
        for sentence in doc:
            for span in sentence.li_spans:
                span.metadata = {
                    name: func(span) for name, func in self.dict_filters.items()
                }
