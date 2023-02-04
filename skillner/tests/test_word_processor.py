from skillner.core.data_structures import Word
from skillner.word_processing.porter_stemmer import PorterStemmer


def test_word_stemming():

    dict_word_stem = {
        "management": "manag",
        "industrial": "industri",
        "extraction": "extract",
    }

    stemmer = PorterStemmer()
    for word, stem in dict_word_stem.items():
        assert stemmer(Word(word)) == stem


if __name__ == "__main__":
    pass
