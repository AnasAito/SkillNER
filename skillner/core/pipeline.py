from typing import Dict

from skillner.core.base import Node
from skillner.core.data_structures import Document


class Pipeline:
    """Pipeline class to define the way of enriching documents.

    The pipeline defines sequential way of enriching documents.

    Attributes
    ----------
    dict_nodes: Dict[str, Node]
        A dictionary that stores the enrichers (nodes) and their
        corresponding names.

    """

    def __init__(self) -> None:
        self.dict_nodes: Dict[str, Node] = {}

    def add_node(self, enricher: Node, name: str) -> None:
        """Append ``enricher`` to the pipeline.

        enricher: instance of Node
            Enricher to be called on the document when pipeline is run.

        name: str
            Name ``enricher`` to identify it among the other enrichers.

        """
        self.dict_nodes[name] = enricher

    def run(self, doc: Document) -> None:
        """Run the pipeline on document.

        Pipeline will call sequentially enricher on the document.

        doc: instance of Document
            Document to enrich.

        """
        for node in self.dict_nodes.values():
            node(doc)
