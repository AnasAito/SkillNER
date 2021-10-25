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
all_cleaning = [
    "remove_punctuation",
    "remove_redundant",
    "stem_text",
    "lem_text",
    "remove_extra_space"
]


# remove punctuation from text
def remove_punctuation(
    text: str,
    list_punctuations: List[str] = LIST_PUNCTUATIONS,
) -> str:
    """To Remove punctuation from a given text.

    Parameters
    ----------
    text : str
        The text to clean.
    list_punctuations: List[str], optional
        A list that define the punctuations to remove, by default LIST_PUNCTUATIONS

    Returns
    -------
    str
        returns a the provided text after removing all punctuations

    Examples
    --------
    >>> from SkillNer.cleaner import remove_punctuation
    >>> text = "Hello there, I am SkillNer! Annoation, annotation, annotation ..."
    >>> print(remove_punctuation(text))
    Hello there  I am SkillNer  Annoation  annotation  annotation
    """

    for punc in list_punctuations:
        text = text.replace(punc, " ")

    # use .strip() to remove extra space in the begining/end of the text
    return text.strip()


# remove redundant words
def remove_redundant(
    text: str,
    list_redundant_words: List[str] = S_GRAM_REDUNDANT,
) -> str:
    """To remove phrases that appear frequently and that can not be used to infere skills.

    Parameters
    ----------
    text : str
        The text to clean.
    list_redundant_words : List[str], optional
        The list of phrases to remove, by default S_GRAM_REDUNDANT

    Returns
    -------
    str
        returns text after removing all redundant words provided in `list_redundant_words`

    Examples
    --------
    >>> from SkillNer.cleaner import remove_redundant
    >>> text = "you have professional experience building React apps, you are familiar with version control using git and GitHub"
    >>> print(remove_redundant(text))
    building React apps,  familiar with version control using git and GitHub
    """

    for phrase in list_redundant_words:
        text = text.replace(phrase, "")

    # use .strip() to remove extra space in the begining/end of the text
    return text.strip()


# stem using a predefined stemer
def stem_text(
    text: str,
    stemmer=PorterStemmer(),
) -> str:
    """To stem a text 

    Parameters
    ----------
    text : str
        The text to be stemmed.
    stemmer : stemmer loaded from nltk, optional
        The stemmer to be used when stemming text, by default PorterStemmer()

    Returns
    -------
    str
        returns text after stemming it.

    Examples
    --------
    >>> from SkillNer.cleaner import stem_text
    >>> text = "you have professional experience building React apps, you are familiar with version control using git and GitHub"
    >>> print(stem_text(text))
    you have profession experi build react apps, you are familiar with version control use git and github
    """

    return " ".join([stemmer.stem(word) for word in text.split(" ")])


# lem text using nlp loaded from scapy
def lem_text(
    text: str,
    nlp,
) -> str:
    """To lem a text.

    Parameters
    ----------
    text : str
        the text to be lemmed
    nlp : nlp object loaded form spacy.
        the nlp used to lem the text

    Returns
    -------
    str
        returns text after lemming it.

    Examples
    --------
    >>> from SkillNer.cleaner import lem_text
    >>> import spacy
    >>> nlp = spacy.load("en_core_web_sm")
    >>> text = "you have professional experience building React apps, you are familiar with version control using git and GitHub"
    >>> print(lem_text(text, nlp))
    you have professional experience building react app , you be familiar with version control use git and GitHub
    """

    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])


# remove extra space
def remove_extra_space(
    text: str,
) -> str:
    """To remove extra space in a given text.

    Parameters
    ----------
    text : str
        The text to clean.

    Returns
    -------
    str
        returns text after removing all redundant spaces.

    Examples
    --------
    >>> from SkillNer.cleaner import remove_extra_space
    >>> text = " I am   sentence with   a lot of  annoying extra    spaces    ."
    >>> print(remove_extra_space(text))
    I am sentence with a lot of annoying extra spaces .
    """

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
    """Function to determine the indexes of words in a phrase given a text.

    Parameters
    ----------
    phrase : str
        the input phrase.
    text : str
        the text where to look for phrase and detemine their indexes

    Returns
    -------
    List[int]
        returns a list of the indexes of words in phrase. An empty list is returned if phrase is not in text.

    Examples
    --------
    >>> from SkillNer.cleaner import find_index_phrase
    >>> text = "you have professional experience building React apps, you are familiar with version control using git and GitHub"
    >>> phrase = "experience building"
    >>> find_index_phrase(phrase, text)
    [3, 4]
    >>> find_index_phrase(phrase="Hello World", text)
    []
    """

    if phrase in text:
        # words in text
        list_words = text.split(" ")

        # words in phrase
        list_phrase_words = phrase.split(" ")
        n = len(list_phrase_words)

        for i in range(len(text) - n):
            if list_words[i:i + n] == list_phrase_words:
                return [i + k for k in range(n)]

    return []


class Cleaner:
    """A class to build pipelines to clean text.
    """

    def __init__(
        self,
        to_lowercase: bool = True,
        include_cleaning_functions: List[str] = all_cleaning,
        exclude_cleaning_function: List[str] = [],
    ):
        """the constructor of the class.

        Parameters
        ----------
        to_lowercase : bool, optional
            whether to lowercase the text before cleaning it, by default True
        include_cleaning_functions : List, optional
            List of cleaning operations to include in the pipeline, by default all_cleaning
        exclude_cleaning_function : List, optional
            List of cleaning operations to exclude for the pipeline, by default []
        """

        # store params
        self.include_cleaning_functions = include_cleaning_functions
        self.exclude_cleaning_functions = exclude_cleaning_function
        self.to_lowercase = to_lowercase

    def __call__(
        self,
        text: str
    ) -> str:
        """To apply the initiallized cleaning pipeline on a given text.

        Parameters
        ----------
        text : str
            text to clean

        Returns
        -------
        str
            returns the text after applying all cleaning operations on it.

        Examples
        -------
        >>> from skillNer.cleaner import Cleaner
        >>> cleaner = Cleaner(
                        to_lowercase=True,
                        include_cleaning_functions=["remove_punctuation", "remove_extra_space"]
                    )
        >>> text = " I am   sentence with   a lot of  annoying extra    spaces    , and !! some ,., meaningless punctuation ?! .! AH AH AH"
        >>> cleaner(text)
        'i am sentence with a lot of annoying extra spaces and some meaningless punctuation ah ah ah'
        """

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
