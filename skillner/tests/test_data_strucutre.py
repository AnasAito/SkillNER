from skillner.core.data_structures import Sentence, Word


def test_to_str():
    sentence = Sentence()

    greeting_sentence = "Hello and welcome to skillner".split()
    sentence.li_words = [Word(w) for w in greeting_sentence]

    assert len(sentence) == len(greeting_sentence)
    assert str(sentence[2]) == greeting_sentence[2]
    assert str(sentence) == " ".join(greeting_sentence)


if __name__ == "__main__":
    pass
