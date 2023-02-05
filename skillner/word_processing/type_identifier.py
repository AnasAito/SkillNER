from skillner.core.data_structures import Word

# define stop words as a set to efficiently look up a word in it
# cf. https://wiki.python.org/moin/TimeComplexity for details about time complexity

# disable black for this line
# fmt: off
STOP_WORDS = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"} # noqa
# fmt: on


class TypeIdentifier:
    """Class to classify a word as ``STANDARD`` or ``STOP_WORD``.

    An instance of ``TypeIdentifier`` has a function-like behavior
    and hence can be called directly on a word.

    Parameters
    ----------
    to_lowercase: bool, default=True
        If ``True``, the word is lowercased before checking it is type.

    """

    def __init__(self, to_lowercase: bool = True) -> None:
        self.to_lowercase = to_lowercase

    def identify_type(self, word: Word) -> str:
        """Identify the type of ``word`` as ``STANDARD`` or ``STOP_WORD``."""
        word = word.lower() if self.to_lowercase else word
        word_type = "STOP_WORD" if word in STOP_WORDS else "STANDARD"

        return word_type

    def __call__(self, word: Word) -> None:
        return self.identify_type(word)
