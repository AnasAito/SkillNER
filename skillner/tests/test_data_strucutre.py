from skillner.core.data_structures import Sentence, Word, Document


def test_to_str():
    greeting = "Hello and welcome to skillner".split()
    purpose = "you can easily extract skills".split()
    text = ".\n".join(
        s for s in (" ".join(splitted_s) for splitted_s in (greeting, purpose))
    )

    doc = Document()
    doc.li_sentences

    for s in (greeting, purpose):
        sentence = Sentence()
        sentence.li_words = [Word(w) for w in s]
        doc.li_sentences.append(sentence)

    assert len(doc) == 2
    assert len(doc[1]) == len(purpose)
    assert str(doc[0]) == " ".join(greeting)
    assert str(doc) == text


if __name__ == "__main__":
    pass
