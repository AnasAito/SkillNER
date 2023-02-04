from typing import Dict, Callable

from skillner.core.base import Node
from skillner.core.data_structures import Document, Word


class WordProcessor(Node):
    """"""

    def __init__(self, dict_filters: Dict[str, Callable[[Word], str]]) -> None:
        # TODO: validate dict_filters
        self.dict_filters = dict_filters

    def enrich_doc(self, doc: Document) -> None:
        """"""
        for sentence in doc:
            for word in sentence:
                word.metadata = {
                    name: func(word) for name, func in self.dict_filters.items()
                }
