from typing import List, Type


class Word(str):
    """Word class.

    A class that behaves as a string with additional metadata stored
    throughout the enrichment of document.

    Parameters
    ----------
    word: str
        a string to initialize word.

    Examples
    --------
    >>> from skillner.core import Word
    >>> w = Word("skillner")
    >>> w
    'skillner'

    """

    def __init__(self, word: str) -> None:
        # word is passed in implicitly to the constructor of str
        # TODO: Validate word namely check it's a word not a phrase
        super().__init__()


class Span:
    def __init__(self, idx_start, idx_end) -> None:
        # TODO: validate idx_start < idx_end
        self.idx_start: int = idx_start
        self.idx_end: int = idx_end

        self.li_candidates: List[dict] = []


class Sentence:
    """Sentence class with sequence-like behavior.

    A sentence is a list of words with additional metadata stored
    throughout the enrichment.

    Examples
    --------
    >>> from skillner.core import Sentence, Word
    >>> s = Sentence()
    >>> s.li_words = [Word(w) for w in "Hello and welcome to skillner".split()]
    >>> len(s)
    5
    >>> s[2]
    'welcome'

    """

    def __init__(self) -> None:
        self.li_words: List[Word] = []

    def __getitem__(self, sl) -> Type[Word]:
        return self.li_words[sl]

    def __str__(self) -> str:
        """Return a the string form of sentence."""
        return " ".join(str(word) for word in self)

    def __len__(self) -> int:
        """Return the number of word in sentence."""
        return len(self.li_words)


class Document:
    """Document class with sequence-like behavior.

    A document is a list of sentences with additional metadata stored
    throughout the enrichment.
    """

    def __init__(self) -> None:
        self.li_sentences: List[Sentence] = []

    def __getitem__(self, sl) -> Type[Sentence]:
        return self.li_sentences[sl]

    def __str__(self) -> str:
        """Return a string form of document."""
        return ".\n".join(str(sentence) for sentence in self)

    def __len__(self) -> int:
        """Return the number of sentences in document."""
        return len(self.li_sentences)
