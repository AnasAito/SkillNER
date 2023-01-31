from typing import List, Type, Dict


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


class Candidate:
    """"""

    def __init__(self, window: slice) -> None:
        self.window = window
        self.metadata: Dict[str, str] = {}

    @property
    def start(self):
        return self.window.start

    @property
    def stop(self):
        return self.window.stop

    def __len__(self) -> int:
        return self.window.stop - self.window.start


class Span:
    """"""

    def __init__(self) -> None:
        self.start: int = None
        self.stop: int = None

        self.li_candidates: List[Candidate] = []

    @property
    def window(self) -> slice:
        """"""
        return slice(self.start, self.stop)

    def add_candidate(self, candidate: Candidate) -> None:
        """"""
        # append candidate
        self.li_candidates.append(candidate)

        # update start and stop of span
        # handle case span freshly created
        if self.is_empty():
            start, stop = candidate.start, candidate.stop
        else:
            start = min(self.start, candidate.start)
            stop = max(self.stop, candidate.stop)

        self.start = start
        self.stop = stop

    def is_empty(self) -> bool:
        """"""
        if len(self.li_candidates) == 0:
            return True

        if self.start == self.stop:
            return True

        return False


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
        self.li_spans: List[Span] = []

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
