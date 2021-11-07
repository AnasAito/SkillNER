# native packs
from typing import List


class Phrase:
    """Data structure to build html visualization of the annotated text.
    The input text is split into skill phrase and non skill phrase
    """

    def __init__(
        self,
        text: str
    ) -> None:

        # save raw text
        self.raw_text = text

        # position of phrase in original text
        self.start: int = None
        self.end: int = None

        # type of phrase: skill or not
        self.is_skill: bool = False

        # meta data
        self.skill_id: str = ""
        self.skill_name: str = ""
        self.skill_type: str = ""  # certification, hard skill or soft skill
        self.score: float = None
        self.type_matching: str = ""  # full match, n_gram

    def get_meta_data(self) -> dict:

        return {
            "skill name": self.skill_name,
            "matching type": self.type_matching,
            "score": self.score
        }

    @staticmethod
    def split_text_to_phare(
        annotation: dict,  # result of skill extractor
        SKILL_DB: dict
    ) -> List:
        """Main function to distinguish skill and non skill phrases

        Parameters
        ----------
        annotation : dict
            The output of the ``SkillExtractor.annotate``
        SKILL_DB: dict
            Data base of skills

        Returns
        -------
        List
            returns a list of phrases
        """
        # params
        list_words = annotation["text"].split(" ")

        # find skill phrases
        arr_skill_phrases = []

        for type_matching, arr_skills in annotation["results"].items():
            for skill in arr_skills:
                # create a phrase object
                phrase = Phrase(text=skill["doc_node_value"])
                phrase.is_skill = True

                # index word start and end
                start = skill["doc_node_id"][0]
                end = skill["doc_node_id"][-1]

                phrase.start = start
                phrase.end = end

                # meta data
                phrase.type_matching = type_matching
                phrase.skill_id = skill["skill_id"]
                phrase.skill_name = SKILL_DB[skill["skill_id"]]["skill_name"]
                phrase.skill_type = SKILL_DB[skill["skill_id"]]["skill_type"]
                phrase.score = skill["score"]

                # append phrase
                arr_skill_phrases.append(phrase)

        # handle case where no skill was annotated in text
        if not len(arr_skill_phrases):
            phrase = Phrase(text=annotation["text"])

            return [phrase]

        # order phrases
        arr_skill_phrases.sort(key=lambda item: item.start)

        # find non skill phrases
        arr_non_skill_phrases = []

        # handle case of first skill phrase
        start = 0
        end = arr_skill_phrases[0].start - 1

        non_skill_phrase = Phrase(" ".join(list_words[start:end + 1]))
        non_skill_phrase.start = start
        non_skill_phrase.end = end

        arr_non_skill_phrases.append(non_skill_phrase)

        # between skills phrases
        for i in range(len(arr_skill_phrases) - 1):
            start = arr_skill_phrases[i].end + 1
            end = arr_skill_phrases[i + 1].start - 1

            non_skill_phrase = Phrase(" ".join(list_words[start:end + 1]))
            non_skill_phrase.start = start
            non_skill_phrase.end = end

            arr_non_skill_phrases.append(non_skill_phrase)

        # handle case of last skill phrase
        # handle case of first skill phrase
        start = arr_skill_phrases[-1].end + 1
        end = len(list_words) - 1

        non_skill_phrase = Phrase(" ".join(list_words[start:end + 1]))
        non_skill_phrase.start = start
        non_skill_phrase.end = end

        arr_non_skill_phrases.append(non_skill_phrase)

        # merge arr non skill and skill then sort
        arr_phrases = arr_skill_phrases + arr_non_skill_phrases
        arr_phrases.sort(key=lambda item: item.start)

        return arr_phrases
