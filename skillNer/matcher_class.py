# native packs
from typing import List
# installed packs
#
# my packs
from skillNer.text_class import Text


class Matchers:
    """class to instanciate a matcher pipeline used to annotate text.
    """

    def __init__(
        self,
        nlp,
        skills_db: dict,
        phraseMatcher
    ):
        """Constructor of the class

        Parameters
        ----------
        nlp : [type]
            NLP object loaded from spacy
        skills_db : dict
            A skill database that serves as a lookup table to annotate text
        phraseMatcher : [type]
            a phraseMatcher loaded using spacy
        """

        # params
        self.nlp = nlp
        self.skills_db = skills_db
        self.phraseMatcher = phraseMatcher
        #self.stop_words = stop_words

        # save matchers in a dict
        self.dict_matcher = {
            'full_matcher': self.get_full_matcher,
            'abv_matcher': self.get_abv_matcher,
            'full_uni_matcher': self.get_full_uni_matcher,
            'low_form_matcher': self.get_low_form_matcher,
            'token_matcher': self.get_token_matcher,
        }

        return

    # load specified matchers
    def load_matchers(
            self,
            include: List[str] = ['full_matcher',
                                  'abv_matcher',
                                  'full_uni_matcher',
                                  'low_form_matcher',
                                  'token_matcher',
                                  ],
            exclude: List[str] = []) -> dict:
        """To load matchers. The order of matchers define a pipeline.

        Parameters
        ----------
        include : List[str], optional
            List of matchers to include in the pipeline, by default ['full_matcher', 'abv_matcher', 'full_uni_matcher', 'low_form_matcher', 'token_matcher', ]
        exclude : List[str], optional
            List of matchers to exclude from the pipeline, by default []

        Returns
        -------
        dict
            returns a dictionnary where the keys are the name of matchers and the values are the matchers

        Examples
        --------
        >>> from skillNer.matcher_class import Matchers
        >>> from skillNer.general_params import SKILL_DB
        >>> import spacy
        >>> from spacy.matcher import PhraseMatcher
        >>> nlp = spacy.load('en_core_web_sm')
        >>> matcher_pipeline = Matchers(nlp, SKILL_DB, PhraseMatcher)
        >>> matcher_pipeline.load_matchers()
        loading full_matcher ...
        loading abv_matcher ...
        loading full_uni_matcher ...
        loading low_form_matcher ...
        loading token_matcher ...

        {'full_matcher': <spacy.matcher.phrasematcher.PhraseMatcher at 0x1c9680b8ac0>,
         'abv_matcher': <spacy.matcher.phrasematcher.PhraseMatcher at 0x1c96c90a6d0>,
         'full_uni_matcher': <spacy.matcher.phrasematcher.PhraseMatcher at 0x1c96c90a7b0>,
         'low_form_matcher': <spacy.matcher.phrasematcher.PhraseMatcher at 0x1c96c90a900>,
         'token_matcher': <spacy.matcher.phrasematcher.PhraseMatcher at 0x1c96c90a820>}
        """

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
    # high confident matchers
    def get_full_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        full_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key

            skill_len = skills_db[key]['skill_len']
            if skill_len > 1:
                skill_full_name = skills_db[key]['high_surfce_forms']['full']
                # add to matcher
                skill_full_name_spacy = nlp.make_doc(skill_full_name)
                full_matcher.add(str(skill_id), [skill_full_name_spacy])

        return full_matcher

    def get_abv_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        abv_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key
            # check if there is a skill abrv
            if 'abv' in skills_db[key]['high_surfce_forms'].keys():
                skill_abv = skills_db[key]['high_surfce_forms']['abv']
                skill_abv_spacy = nlp.make_doc(skill_abv)
                abv_matcher.add(str(skill_id), [skill_abv_spacy])

        return abv_matcher

    def get_full_uni_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        full_uni_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key

            skill_len = skills_db[key]['skill_len']
            if skill_len == 1:
                skill_full_name = skills_db[key]['high_surfce_forms']['full']
                # add to matcher
                skill_full_name_spacy = nlp.make_doc(skill_full_name)
                full_uni_matcher.add(str(skill_id), [skill_full_name_spacy])

        return full_uni_matcher

    # low confident matchers
    def get_low_form_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        low_form_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:

            # get skill info
            skill_id = key
            skill_len = skills_db[key]['skill_len']

            low_surface_forms = skills_db[key]['low_surface_forms']
            for form in low_surface_forms:
                skill_form_spacy = nlp.make_doc(form)
                low_form_matcher.add(str(skill_id), [skill_form_spacy])
        return low_form_matcher

    def get_token_matcher(self):
        # params
        nlp = self.nlp
        skills_db = self.skills_db
        token_matcher = self.phraseMatcher(nlp.vocab, attr="LOWER")

        # populate matcher
        for key in skills_db:
            # get skill info
            skill_id = key
            match_on_tokens = skills_db[key]['match_on_tokens']

            if match_on_tokens:  # check if skill accept matches on its unique tokens
                skill_lemmed = skills_db[key]['high_surfce_forms']['full']
                skill_lemmed_tokens = skill_lemmed.split(' ')

                # add tokens to matcher
                for token in skill_lemmed_tokens:
                    # give id that ref 1_gram matching
                    if token.isdigit():
                        pass
                    else:
                        id_ = skill_id
                        token_matcher.add(str(id_), [nlp.make_doc(token)])

        return token_matcher


class SkillsGetter:
    """Class that gather functions to get the matched skills.
    """

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
        doc = self.nlp(text_obj.lemmed())

        for match_id, start, end in matcher(doc):
            id_ = matcher.vocab.strings[match_id]
            # add full_match to store
            skills.append({'skill_id': id_,
                           'doc_node_value': str(doc[start:end]),
                           'score': 1,
                           'doc_node_id': list(range(start, end))})
            # mutate text tokens metadata (unmatch attr)
            for token in text_obj[start:end]:
                token.is_matchable = False

        return skills, text_obj

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
                               'score': 1,
                               'doc_node_value': str(doc[start:end]),
                               'doc_node_id': [start]})
                # mutate matched tokens
                for token in text_obj[start:end]:
                    token.is_matchable = False

        return skills, text_obj

    def get_full_uni_match_skills(
        self,
        text_obj: Text,
        matcher
    ):

        skills = []

        doc = self.nlp(text_obj.transformed_text)
        for match_id, start, end in matcher(doc):
            id_ = matcher.vocab.strings[match_id]
            if text_obj[start].is_matchable:
                skills.append({'skill_id': id_+'_fullUni',
                               'score': 1,
                               'doc_node_value': str(doc[start:end]),
                               'doc_node_id': [start],
                               'type': 'full_uni'})

        return skills, text_obj

    def get_token_match_skills(
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

            # add
            if text_obj[start].is_matchable:
                skills.append({'skill_id': id_+'_oneToken',
                               'doc_node_value': str(doc[start:end]),
                               'doc_node_id': [start],
                               'type': 'one_token'})

        return skills

    def get_low_match_skills(
        self,
        text_obj: Text,
        matcher
    ):

        skills = []
        doc = self.nlp(text_obj.stemmed())

        for match_id, start, end in matcher(doc):
            id_ = matcher.vocab.strings[match_id]

            if text_obj[start].is_matchable:
                skills.append({'skill_id': id_+'_lowSurf',
                               'doc_node_value': str(doc[start:end]),
                               'doc_node_id': list(range(start, end)),
                               'type': 'lw_surf'})

        return skills, text_obj
