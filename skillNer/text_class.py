# native packs
from typing import List
# installed packs
#
# my packs
from skillNer.cleaner import Cleaner, stem_text, find_index_phrase
from skillNer.general_params import S_GRAM_REDUNDANT


# building block of text
class Word:
    def __init__(
        self,
        word: str
    ):

        # immutable version of word
        self.word = word

        # attributes
        self.lemmed = ""
        self.stemmed = ""

        self.is_stop_word = None
        self.is_matchable = True

        # position in sentence
        self.start: int
        self.end: int
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

    # give the len of the word
    def __len__(self):
        return len(self.word)


class Text:
    def __init__(
        self,
        text: str,
        nlp
    ):

        # immutable version of text
        self.immutable_text = text

        # transformed text: lower + punctuation + extra space
        # this is the version of text that we will be working with
        cleaner = Cleaner(include_cleaning_functions=[
                          "remove_punctuation", "remove_extra_space"], to_lowercase=False,)

        self.transformed_text = cleaner(text).lower()
        # abv version
        self.abv_text = cleaner(text)

        # list that holds all words within text
        self.list_words = []

        # construct list of words and create meta data object
        doc = nlp(self.transformed_text)

        for token in doc:
            # create word object
            word = Word(token.text)

            # lem and stem
            word.lemmed = token.lemma_
            word.stemmed = stem_text(token.text)

            # stop word and machability
            word.is_stop_word = token.is_stop
            # a stop word is unmatchable
            if token.is_stop:
                word.is_matchable = False

            self.list_words.append(word)

        # detect unmatchable words
        for redundant_word in S_GRAM_REDUNDANT:
            list_index = find_index_phrase(
                phrase=redundant_word, text=self.transformed_text)

            for index in list_index:
                self[index].is_matchable = False

    # return stemmed form of text either as str or list of words
    def stemmed(self, as_list: bool = False):
        list_stems = [word.stemmed for word in self.list_words]

        if as_list:
            return list_stems

        return " ".join(list_stems)

    # return lemmed form of text either as str or list of words
    def lemmed(self, as_list: bool = False):
        list_lems = [word.lemmed for word in self.list_words]

        if as_list:
            return list_lems

        return " ".join(list_lems)

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

    # result a list of word object
    # each word contain the info of its start/end position
    @staticmethod
    def words_start_end_position(text: str):
        # words in text
        list_words = []

        pointer = 0
        for raw_word in text.split(" "):
            # init object word
            word = Word(raw_word)

            # start and end of word
            word.start = pointer
            word.end = pointer + len(word)

            # update pointer
            pointer += len(word) + 1

            list_words.append(word)

        return list_words
