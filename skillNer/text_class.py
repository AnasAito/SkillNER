# native packs
from typing import List
# installed packs
#
# my packs
from skillNer.cleaner import Cleaner, stem_text, find_index_phrase
from skillNer.general_params import S_GRAM_REDUNDANT


# building block of text
class Word:
    """Main data structure to hold metadata of words
    """

    def __init__(
        self,
        word: str
    ) -> None:
        """Construct an instance of Word

        Parameters
        ----------
        word : str
            The word is given as string

        Examples
        --------
        >>> from skillNer.text_class import Word
        >>> word_obj = Word("Hello")
        """

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
    def metadata(self) -> dict:
        """To get all metadata of the instance

        Returns
        -------
        dict
            dictionnary containing all metadata of object. Look at the example to see the returned keys

        Examples
        --------
        >>> from skillNer.text_class import Word
        >>> word_obj = Word("Hello")
        >>> word_obj.metadata().keys()
        dict_keys(['lemmed', 'stemmed', 'is_stop_word', 'is_matachable'])
        """

        return {
            "lemmed": self.lemmed,
            "stemmed": self.stemmed,
            "is_stop_word": self.is_stop_word,
            "is_matachable": self.is_matchable
        }

    # give the raw version of word when transformed to str
    def __str__(self) -> str:
        """To get the raw form of word

        Returns
        -------
        str
            raw form of word

        Examples
        --------
        >>> from skillNer.text_class import Word
        >>> word_obj = Word("Hello")
        >>> print(word_obj)
        Hello
        """
        return self.word

    # give the len of the word
    def __len__(self) -> int:
        """Gives the number of characters in word

        Returns
        -------
        int
            returns the number of characters in word

        Examples
        --------
        >>> from skillNer.text_class import Word
        >>> word_obj = Word("Hello")
        >>> len(word_obj)
        5
        """
        return len(self.word)


class Text:
    """The main object to store/preprocess a raw text. 
    The object behaviour is like a list according to words.
    """

    def __init__(
        self,
        text: str,
        nlp
    ):
        """Constructor of the class

        Parameters
        ----------
        text : str
            The raw text. It might be for instance a job description.
        nlp : [type]
            An NLP object instanciated from Spacy.

        Examples
        --------
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_sm')
        >>> from skillNer.text_class import Text
        >>> text_obj = Text("Fluency in both English and French is mandatory")
        """

        # immutable version of text
        self.immutable_text = text

        # transformed text: lower + punctuation + extra space
        # this is the version of text that we will be working with
        cleaner = Cleaner(
            include_cleaning_functions=[
                "remove_punctuation",
                "remove_extra_space"
            ],
            to_lowercase=False
        )

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
    def stemmed(
        self,
        as_list: bool = False
    ):
        """To get the stemmed version of text

        Parameters
        ----------
        as_list : bool (default False)
            True to get a list of stemmed words within text. False, to get stemmed text in a form of string.

        Returns
        -------
        str | List[str]
            return the stemmed text in the specified form by the argument `as_list`.

        Examples
        --------
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_sm')
        >>> from skillNer.text_class import Text
        >>> text_obj = Text("Fluency in both English and French is mandatory")
        >>> text_obj.stemmed()
        'fluenci in both english and french is mandatori'
        >>> text_obj.stemmed(as_list=True)
        ['fluenci', 'in', 'both', 'english', 'and', 'french', 'is', 'mandatori']
        """

        list_stems = [word.stemmed for word in self.list_words]

        if as_list:
            return list_stems

        return " ".join(list_stems)

    # return lemmed form of text either as str or list of words
    def lemmed(
        self,
        as_list: bool = False
    ):
        """To get the lemmed version of text

        Parameters
        ----------
        as_list : bool
            True to get a list of lemmed words within text. False, to get lemmed text in a form of string.

        Returns
        -------
        str | List[str]
            return the lemmed text in the specified form by the argument `as_list`

        Examples
        --------
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_sm')
        >>> from skillNer.text_class import Text
        >>> text_obj = Text("Fluency in both English and French is mandatory")
        >>> text_obj.lemmed()
        'fluency in both english and french be mandatory'
        >>> text_obj.lemmed(as_list=True)
        ['fluency', 'in', 'both', 'english', 'and', 'french', 'be', 'mandatory']
        """

        list_lems = [word.lemmed for word in self.list_words]

        if as_list:
            return list_lems

        return " ".join(list_lems)

    # return raw version of text when converted to str
    def __str__(self) -> str:
        """To get the raw version of text

        Returns
        -------
        str
            returns the raw version of text

        Examples
        --------
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_sm')
        >>> from skillNer.text_class import Text
        >>> text_obj = Text("Fluency in both English and French is mandatory")
        >>> print(text_obj)
        Fluency in both English and French is mandatory
        """

        return self.immutable_text

    # equip text with the behavior of a list
    # get item with []
    def __getitem__(
        self,
        index: int
    ) -> Word:
        """To get the word at the specified position by index

        Parameters
        ----------
        index : int
            the position of the word

        Returns
        -------
        Word
            returns thhe word object in the index-position

        Examples
        --------
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_sm')
        >>> from skillNer.text_class import Text
        >>> text_obj = Text("Fluency in both English and French is mandatory")
        >>> text_obj[3]
        <skillNer.text_class.Word at 0x1cf13a9bd60>
        >>> print(text_obj[3])
        english
        """
        return self.list_words[index]

    # len of a text is the number of words in it
    def __len__(self) -> int:
        """To get the number of words in text

        Returns
        -------
        int
            returns the number of words in text

        Examples
        --------
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_sm')
        >>> from skillNer.text_class import Text
        >>> text_obj = Text("Fluency in both English and French is mandatory")
        >>> len(text_obj)
        8
        """

        return len(self.list_words)

    # result a list of word object
    # each word contain the info of its start/end position
    @staticmethod
    def words_start_end_position(text: str) -> List[Word]:
        """To get the starting and ending index of each word in text

        Parameters
        ----------
        text : str
            The input text

        Returns
        -------
        List[Word]
            Returns a list of words where in each word the `start` and `end` 
            properties were filled by the starting and ending position of the word.

        Examples
        --------
        >>> import spacy
        >>> nlp = spacy.load('en_core_web_sm')
        >>> from skillNer.text_class import Text
        >>> list_words = Text.words_start_end_position("Hello World I am SkillNer")
        >>> word_1 = list_words[0]
        >>> print(word_1.start, word_1.end)
        0 5
        """
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
