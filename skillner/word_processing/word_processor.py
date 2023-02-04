from typing import Dict, Callable

from skillner.core.base import Node
from skillner.core.data_structures import Document, Word


class WordProcessor(Node):
    """Word preprocessor class that runs functions on all words of document.

    ``WordPreprocessor`` class acts on individual words of document. It runs
    independently functions and stores the result on the ``metadata``
    dictionary of word.

    Parameters
    ----------
    dict_filters: Dict[str, Callable[[Word], str]]
        A dictionary of functions that take Word as input and returns a string.

    """

    def __init__(self, dict_filters: Dict[str, Callable[[Word], str]]) -> None:
        # TODO: validate dict_filters
        self.dict_filters = dict_filters

    def enrich_doc(self, doc: Document) -> None:
        """Enrich every word of ``doc``.

        Parameters
        ----------
        doc: Document
            The document in which to find spans.

        """
        for sentence in doc:
            for word in sentence:
                word.metadata = {
                    name: func(word) for name, func in self.dict_filters.items()
                }
