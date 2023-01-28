from abc import abstractmethod

from skillner.core.data_structures import Document


class Node:
    """"""

    @abstractmethod
    def enrich_doc(self, doc: Document) -> None:
        """"""

    def __call__(self, doc: Document) -> None:
        """"""
        self.enrich_doc(doc)
