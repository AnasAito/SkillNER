# native packs
from typing import List
# installed packs
# 
# my packs
from skillNer.cleaner import Cleaner, stem_text, lem_text, find_index_phrase, nlp
from skillNer.general_params import s_gram_redundant


# building block of text
class Word:
    def __init__(self, word: str):
        # immutable version of word
        self.word = word

        # attributes
        self.lemmed = ""
        self.stemmed = ""

        self.is_stop_word = None
        self.is_matchable = True
        pass
    
    # get metadata of word
    def metadata(self):
        return {
            "lemmed": self.lemmed,
            "stemmed": self.stemmed,
            "is_stop_word": self.is_stop_word,
            "is_matachable": self.is_matchable
        }

    # give the raw version of word when transformed to str
    def __str__(self):
        return self.word


class Text:
    def __init__(self, text: str, nlp=nlp):
        # immutable version of text
        self.immutable_text = text

        # transformed text: lower + punctuation + extra space
        # this is the version of text that we will be working with
        cleaner = Cleaner(include_cleaning_functions=["remove_punctuation", "remove_extra_space"])
        self.transformed_text = cleaner(text)

        # list of words within text
        self.list_words = []
        for raw_word in self.transformed_text.split(" "):
            word = Word(raw_word)

            # add attributes
            word.stemmed = stem_text(raw_word)
            word.lemmed = lem_text(raw_word, nlp=nlp)

            self.list_words.append(word)

        # detect stop words
        doc = nlp(self.transformed_text)

        for token, i in zip(doc, range(len(self))):
            self[i].is_stop_word = token.is_stop

            # a stop word is unmatchable
            if token.is_stop:
                self[i].is_matchable = False

        # detect unmatchable words
        for redundant_word in s_gram_redundant:
            list_index = find_index_phrase(phrase=redundant_word, text=self.transformed_text)

            for index in list_index:
                self[index].is_matchable = False
    
    def stemmed(self):
        return " ".join([word.stemmed for word in self.list_words])

    def lemmed(self):
        return " ".join([word.lemmed for word in self.list_words])

    # return raw version of text when converted to str
    def __str__(self):
        return self.immutable_text

    # equip text with the behavior of a list
    # get item with []
    def __getitem__(self, index) -> Word:
        return self.list_words[index]

    # len of a text is the number of words in it
    def __len__(self):
        return len(self.list_words)
