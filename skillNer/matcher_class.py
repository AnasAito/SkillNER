# native packs
from typing import List
# installed packs
#
# my packs
from skillNer.text_class import Text


class Matchers:
    def __init__(
        self,
        nlp,
        skills_db: dict,
        phraseMatcher,
        stop_words: List[str]
    ):

        # params
        self.nlp = nlp
        self.skills_db = skills_db
        self.phraseMatcher = phraseMatcher
        self.stop_words = stop_words

        # save matchers in a dict
        self.dict_matcher = {
            'full_matcher': self.get_full_matcher,
            'ngram_matcher': self.get_ngram_matcher,
            'uni_gram_matcher': self.get_uni_gram__matcher,
            'abv_matcher': self.get_abv_matcher}

        return

    # load specified matchers
    def load_matchers(self, include=['full_matcher', 'ngram_matcher', 'uni_gram_matcher', 'abv_matcher'], exclude=[]):

        # #where to store loaded matchers
        loaded_matchers = {}

        # load matchers in if exclude is not empty
        # include will ignored
        if len(exclude):
            for matcher_name, matcher in self.dict_matcher.items():
                if matcher_name not in exclude:
                    print(f"loading {matcher_name} ...")
                    loaded_matchers[matcher_name] = matcher()
        else:
            for matcher_name, matcher in self.dict_matcher.items():
                if matcher_name in include:
                    print(f"loading {matcher_name} ...")
                    loaded_matchers[matcher_name] = matcher()

        return loaded_matchers

    # matchers
    def get_full_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        full_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key
            skill_full_name = skills_db[key]['skill_cleaned']
            skill_len = skills_db[key]['skill_len']
            if skill_len > 1:
                # add to matcher
                skill_full_name_spacy = nlp.make_doc(skill_full_name)
                full_matcher.add(str(skill_id), [skill_full_name_spacy])

        return full_matcher

    def get_ngram_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        ngram_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key
            skill_lemmed = skills_db[key]['skill_lemmed']
            skill_lemmed_tokens = [w for w in skill_lemmed.split(' ')
                                   if not(w in self.stop_words or w.isdigit())]

            skill_len = skills_db[key]['skill_len']
            if skill_len > 1:  # add only ngram skills
                # add full_stemed to matcher
                skill_lemmed_spacy = nlp.make_doc(skill_lemmed)
                ngram_matcher.add(str(skill_id), [skill_lemmed_spacy])
                # add tokens to matcher
                for token in skill_lemmed_tokens:
                    # give id that ref 1_gram matching
                    id_ = skill_id+'_1w'
                    ngram_matcher.add(str(id_), [nlp.make_doc(token)])

        return ngram_matcher

    def get_uni_gram__matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        single_gram_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key
            skill_stemmed = skills_db[key]['skill_stemmed']
            skill_len = skills_db[key]['skill_len']
            if skill_len == 1:
                # add to matcher
                skill_stemmed_spacy = nlp.make_doc(skill_stemmed)
                single_gram_matcher.add(str(skill_id), [skill_stemmed_spacy])

        return single_gram_matcher

    def get_abv_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        abv_matcher = self.phraseMatcher(nlp.vocab)

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key
            skill_abv = skills_db[key]['abbreviation']

            skill_abv_spacy = nlp.make_doc(skill_abv)
            abv_matcher.add(str(skill_id), [skill_abv_spacy])

        return abv_matcher


class SkillsGetter:
    def __init__(
        self,
        nlp
    ):

        # param
        self.nlp = nlp
        return

    def get_full_match_skills(
        self,
        text_obj: Text,
        matcher
    ):

        skills = []
        doc = self.nlp(text_obj.transformed_text)

        for match_id, start, end in matcher(doc):
            id_ = matcher.vocab.strings[match_id]
            # add full_match to store
            skills.append({'skill_id': id_,
                           # 'doc_node_value': str(doc[start:end]),
                           'score': 1,
                           'doc_node_id': list(range(start, end))})
            # mutate text tokens metadata (unmatch attr)
            for token in text_obj[start:end]:
                token.is_matchable = False

        return skills, text_obj

    def get_sub_match_skills(
        self,
        text_obj: Text,
        matcher
    ):

        skills_full = []
        skills = []
        sub_matches = []
        full_matches = []

        doc = self.nlp(text_obj.lemmed())
        for match_id, start, end in matcher(doc):
            id_ = matcher.vocab.strings[match_id]
            if '_1w' in id_:
                sub_matches.append((id_, match_id, start, end))
            else:
                full_matches.append((id_, match_id, start, end))

        for match in full_matches:
            id_, match_id, start, end = match
            # full matches no need for scoring
            # check if any intersection betwenn full matcher and sub matcher (priority to full)
            is_matchable = [1 for token in text_obj[start:end]
                            if token.is_matchable]
            if len(is_matchable) != 0:

                skills_full.append({'skill_id': id_,
                                    'score': 1,
                                    # 'doc_node_value': str(doc[start:end]),
                                    'doc_node_id': list(range(start, end))})

                # mutate text tokens metadata (unmatch attr) - only in full match stemmed (100% confident )
                for token in text_obj[start:end]:
                    token.is_matchable = False

        for match in sub_matches:
            id_, match_id, start, end = match
            # add unigram macthes only if not matched in parent modules or not stop word
            if text_obj[start].is_matchable and (not text_obj[start].is_stop_word):
                skills.append({'skill_id': id_,
                               'doc_node_value': str(doc[start:end]),
                               'doc_node_id': start})

        return skills_full, skills, text_obj

    def get_single_match_skills(
        self,
        text_obj: Text,
        matcher
    ):

        skills = []

        doc = self.nlp(text_obj.stemmed())
        for match_id, start, end in matcher(doc):
            id_ = matcher.vocab.strings[match_id]
            if text_obj[start].is_matchable:
                skills.append({'skill_id': id_,
                               'doc_node_value': str(doc[start:end]),
                               'doc_node_id': start})

        return skills

    def get_abv_match_skills(
        self,
        text_obj: Text,
        matcher
    ):
        skills = []

        doc = self.nlp(text_obj.abv_text)
        for match_id, start, end in matcher(doc):
            id_ = matcher.vocab.strings[match_id]
            if text_obj[start].is_matchable:
                skills.append({'skill_id': id_,
                               'doc_node_value': str(doc[start:end]),
                               'doc_node_id': [start]})

        return skills
