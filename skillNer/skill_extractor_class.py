# native packs
# 
# installed packs
#
# my packs
from skillNer.text_class import Text
from skillNer.matcher_class import Matchers, SkillsGetter
from skillNer.utils import Utils


class SkillExtractor:
    def __init__(
        self,
        nlp,
        skills_db,
        phraseMatcher,
        stop_words,
        ):

        # params
        self.nlp = nlp
        self.skills_db = skills_db
        self.phraseMatcher = phraseMatcher
        self.stop_words = stop_words

        # load matchers: all
        self.matchers = Matchers(
            self.nlp, 
            self.skills_db, 
            self.phraseMatcher, 
            self.stop_words
            ).load_matchers()
        
        # init skill getters
        self.skill_getters = SkillsGetter(self.nlp)

        # init utils
        self.utils = Utils(self.nlp, self.skills_db)
        return

    def __call__(
        self,
        text: str
        ):

        # create text object
        text_obj = Text(text, self.nlp)

        # match text
        skills_full, text_obj = self.skill_getters.get_full_match_skills(text_obj, self.matchers['full_matcher'])
        skills_sub_full, skills_ngram, text_obj = self.skill_getters.get_sub_match_skills(text_obj, self.matchers['ngram_matcher'])
        skills_uni = self.skill_getters.get_single_match_skills(text_obj, self.matchers['uni_gram_matcher'])

        # process filter
        n_gram_pro = self.utils.process_n_gram(skills_ngram, text_obj)
        uni_gram_pro = self.utils.process_unigram(skills_uni, text_obj)

        return { 
            'full_match':skills_full, 
            'ngram_full_match':skills_sub_full,
            'ngram_scored':n_gram_pro,
            'unigram_scored':uni_gram_pro
        }