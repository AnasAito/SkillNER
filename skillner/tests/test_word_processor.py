from skillner.core.data_structures import Word, Sentence, Document

from skillner.word_processing.word_processor import WordProcessor
from skillner.word_processing.porter_stemmer import PorterStemmer
from skillner.word_processing.type_identifier import TypeIdentifier


class TestWordPreprocessor:
    dict_word_stem = {
        "management": "manag",
        "industrial": "industri",
        "extraction": "extract",
    }

    text = (
        "i was a student now i am an industrial management "
        "engineer graduated from EMINES"
    )

    def test_porter_stemmer(self):
        stemmer = PorterStemmer()

        for word, stem in self.dict_word_stem.items():
            assert stemmer(Word(word)) == stem

    def test_word_processing(self):

        # init doc with one sentence
        sentence = Sentence()
        sentence.li_words = [Word(s) for s in self.text.split()]

        doc = Document()
        doc.li_sentences.append(sentence)

        stemmer = PorterStemmer()
        type_identifier = TypeIdentifier()

        word_processor = WordProcessor(
            dict_filters={
                "stem": stemmer,
                "lowercase": lambda word: word.lower(),
                "type": type_identifier,
            }
        )
        word_processor(doc)

        assert len(doc[0][0].metadata) == 3
        assert "stem" in doc[0][2].metadata
        assert "lowercase" in doc[0][2].metadata
        assert doc[0][1].metadata["type"] == "STOP_WORD"


if __name__ == "__main__":
    pass
