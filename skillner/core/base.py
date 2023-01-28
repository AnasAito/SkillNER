from abc import abstractmethod

from skillner.core.data_structures import Document


class Node:
    """Base for pipeline building blocks."""

    @abstractmethod
    def enrich_doc(self, doc: Document) -> None:
        """Apply a transformation on ``doc``."""

    def __call__(self, doc: Document) -> None:
        self.enrich_doc(doc)
