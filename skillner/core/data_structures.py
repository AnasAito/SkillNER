from typing import List


class Document:
    """"""

    def __init__(self) -> None:
        pass


class Word:
    """"""

    def __init__(self, word) -> None:
        self.word = word

    def __str__(self) -> str:
        return self.word


class Sentence:
    """"""

    def __init__(self) -> None:
        self.li_words: List[Word]

    def __getitem__(self, i):
        return self.li_words[i]

    def __str__(self) -> str:
        return " ".join(str(word) for word in self)

    def __len__(self):
        return len(self.li_words)
