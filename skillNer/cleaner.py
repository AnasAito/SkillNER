# installed packs
from nltk.stem import PorterStemmer
# import en_core_web_lg
# native packs
from typing import List
# my pack
from skillNer.general_params import S_GRAM_REDUNDANT, LIST_PUNCTUATIONS


# load nlp
# nlp = en_core_web_lg.load()
# list of cleaning functions names
all_cleaning = ["remove_punctuation", "remove_redundant",
                "stem_text", "lem_text", "remove_extra_space"]


# remove punctuation from text
def remove_punctuation(
    text: str,
    *args, **kwargs
) -> str:

    for punc in LIST_PUNCTUATIONS:
        text = text.replace(punc, " ")

    return text.strip()

# remove redundant words


def remove_redundant(
    text: str,
    list_redundant_words: List[str] = S_GRAM_REDUNDANT,
    *args, **kwargs
) -> str:

    for phrase in list_redundant_words:
        text = text.replace(phrase, "")

    return text

# stem using a predefined stemer


def stem_text(
    text: str,
    stemmer=PorterStemmer(),
    *args, **kwargs
) -> str:

    return " ".join([stemmer.stem(word) for word in text.split(" ")])

# lem text using nlp loaded from scapy


def lem_text(
    text: str,
    nlp,
    *args, **kwargs
) -> str:

    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

# remove extra space


def remove_extra_space(
    text: str,
    *args, **kwargs
) -> str:

    return " ".join(text.split())


# gather all cleaning functions in a dict
dict_cleaning_functions = dict_cleaning_functions = {
    "remove_punctuation": remove_punctuation,
    "remove_redundant": remove_redundant,
    "stem_text": stem_text,
    "lem_text": lem_text,
    "remove_extra_space": remove_extra_space
}


# find index of words of a phrase in a text
# return an empty list if phrase not in text
def find_index_phrase(
    phrase: str,
    text: str,
) -> List[int]:

    if phrase in text:
        # words in text
        list_words = text.split(" ")

        # words in phrase
        list_phrase_words = phrase.split(" ")
        n = len(list_phrase_words)

        for i in range(len(text) - len(list_phrase_words)):
            if list_words[i:i + n] == list_phrase_words:
                return [i + k for k in range(n)]

    return []


class Cleaner:
    def __init__(
        self,
        to_lowercase: bool = True,
        include_cleaning_functions: list = all_cleaning,
        exclude_cleaning_function: list = []
    ) -> None:

        # store params
        self.include_cleaning_functions = include_cleaning_functions
        self.exclude_cleaning_functions = exclude_cleaning_function
        self.to_lowercase = to_lowercase

    def __call__(
        self,
        text: str
    ) -> str:

        # lower the provided text
        if(self.to_lowercase):
            text = text.lower()

        # perform cleaning while ignoring exclude_cleaning_functions
        if len(self.exclude_cleaning_functions):
            for cleaning_name in dict_cleaning_functions.keys():
                if cleaning_name not in self.exclude_cleaning_functions:
                    text = dict_cleaning_functions[cleaning_name](text)
        # if exclude_cleaning_functions was provided then include-cleaning_functions will be ignoned
        else:
            for cleaning_name in dict_cleaning_functions.keys():
                if cleaning_name in self.include_cleaning_functions:
                    text = dict_cleaning_functions[cleaning_name](text)

        return text
