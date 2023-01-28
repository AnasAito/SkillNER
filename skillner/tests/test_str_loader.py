from skillner.core.data_structures import Document
from skillner.text_loaders.str_text import StrTextLoader


def test_str_loader():
    # text contains four sentences
    #   - sentence 0: skillNER NER Named Entity Recognition
    #   - sentence 1: is about finding needles skills in a knowledge graph
    #   - sentence 2: never mind that's all about testing on several Case++
    #   - sentence 3: wait what if I was F**ck** meaning it
    text = """
    skillNER, NER:(Named Entity Recognition)! is about finding needles; (skills) in a
    knowledge graph... never mind \n that's all about testing ,on \t
    several Case++. wait ; what if I was F**ck** meaning it .?!
    """

    # sanity check for sentence to words
    sentence = StrTextLoader._sentence2words("(skillner), and((other;  staff ")
    assert str(sentence) == "skillner and other staff"

    doc = Document()
    str_loader = StrTextLoader(text)
    str_loader(doc)

    assert len(doc) == 4
    assert str(doc[1]) == "is about finding needles skills in a knowledge graph"
    assert str(doc[2][2]) == "that's"
