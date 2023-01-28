import re
from typing import List

from skillner.core.data_structures import Document, Sentence, Word
from skillner.core.base import Node


class StrTextLoader(Node):
    """Loader of text as string.

    Used in a pipeline to create the sentences of document.

    Parameters
    ----------
    text: str
        text used to create the document sentences.

    """

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def enrich_doc(self, doc: Document) -> None:
        """Create document sentences.

        Parameters
        ----------
        doc: Document
            The document to enrich with sentences.

        """
        # well format text by substituting \n, \t, space, \v with space
        escape_patterns = r"\s+"
        self.text = re.sub(escape_patterns, repl=" ", string=self.text)
        self.text = self.text.strip()

        # sentence is delimited by . ? or !
        # TODO: use number of words to define sentence
        sentence_pattern = r"[.|?|!]+"

        li_sentences: List[Sentence] = []

        for matched in re.split(sentence_pattern, string=self.text):
            # skip empty string
            if len(matched) == 0:
                continue

            li_sentences.append(StrTextLoader._sentence2words(matched))

        doc.li_sentences = li_sentences

    @staticmethod
    def _sentence2words(raw_sentence: str) -> Sentence:
        # private static method to create words in sentences
        word_pattern = r"[,|;|:| |(|)]+"

        li_words: List[Word] = []

        for word in re.split(word_pattern, string=raw_sentence):
            # skip of empty or space character
            if len(word) == 0 or word == " ":
                continue

            li_words.append(Word(word))

        sentence = Sentence()
        sentence.li_words = li_words

        return sentence
