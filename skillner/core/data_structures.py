from typing import List, Type


class Word:
    """"""

    def __init__(self, word: str) -> None:
        self.word: str = word

    def __str__(self) -> str:
        return self.word


class Sentence:
    """"""

    def __init__(self) -> None:
        self.li_words: List[Word]

    def __getitem__(self, i) -> Type[Word]:
        return self.li_words[i]

    def __str__(self) -> str:
        return " ".join(str(word) for word in self)

    def __len__(self) -> int:
        return len(self.li_words)


class Document:
    """"""

    def __init__(self) -> None:
        self.li_sentences: List[Sentence] = []

    def __getitem__(self, i) -> Type[Sentence]:
        return self.li_sentences[i]

    def __str__(self) -> str:
        return ".\n".join(str(sentence) for sentence in self)

    def __len__(self) -> int:
        return len(self.li_sentences)
