import re
import os
from typing import Any, Dict, List
from collections import Counter
import json
from abc import ABC, abstractmethod

import en_core_web_lg
import tqdm

from skillNer.cleaner import lem_text, stem_text
import fetch_raw_data

ID, NAME, TYPE = "id", "name", "type"
SKILL_NAME, SKILL_CLEANED, SKILL_TYPE, SKILL_LEMMED, \
SKILL_STEMMED, SKILL_LEN, ABBREVIATION, MATCH_ON_STEMMED = "skill_name", "skill_cleaned", "skill_type", \
                                                           "skill_lemmed", "skill_stemmed", "skill_len", \
                                                           "abbreviation", "match_on_stemmed"
HIGH_SURFACE_FORMS, LOW_SURFACE_FORMS, MATCH_ON_TOKENS = "high_surfce_forms", "low_surface_forms", "match_on_tokens"

FILE_SAVE_PATH = os.path.join(os.path.realpath('..'), "skill_data")
SKILL_PROCESSED_FNAME, TOKEN_DIST_FNAME, FINAL_SKILL_FNAME = "skills_processed.json", \
                                                             "token_dist.json",\
                                                             "skill_db_relax_20.json"


def _count_token_dist(long_skill_titles: List[str]) -> Dict[str, int]:
    """generate token distribution in skill titles"""
    words = [token for skill_title in long_skill_titles for token in skill_title.split(' ')]
    dist_dict = dict(Counter(words))
    return dist_dict


class BaseSkillProcessor(ABC):
    """Abstract class for loading the final processes skill list and/or its intermediate files. Will create if not exist.
    Contains abstract methods, can only be used as parent class instead of instantiated directly."""
    def __init__(self):
        self.nlp = en_core_web_lg.load()

    @property
    @abstractmethod
    def skill_list_name(self) -> str:
        """unique skill list name for displaying in progress bar. Must be defined by the subclass"""

    @abstractmethod
    def fetch_raw_skill_list(self) -> List[dict]:
        """method for fetching the corresponding raw skill data, in form of json records of format
        [{'id':'...', 'name': '...', 'type': ...}]"""

    @abstractmethod
    def _get_abbr(self, skill_record) -> str:
        """determines the abbr of a skill; may be empty string only due to no rules defined and no data provided"""

    def preprocess_raw_skills(self, regenerate: bool=False, skill_records: List[dict]=None) -> Dict[str, Dict[str, Any]]:
        """preprocesses skill records.
        Loads skills_records from custom defined fetch_raw_skill_list method if not provided.
        If skill_records provided, the expected skill_records format: [{'id':'...', 'name': '...', 'type': ...}].
        Output format:
            "KS120P86XDXZJT3B7KVJ": {
            "skill_name": "(American Society For Quality) ASQ Certified",
            "skill_cleaned": "asq certified",
            "skill_type": "Certification",
            "skill_lemmed": "asq certify",
            "skill_stemmed": "asq certifi",
            "skill_len": 2,
            "abbreviation": "",
            "match_on_stemmed": false
        }
        """
        processed_skill_path = self.__generate_save_path(SKILL_PROCESSED_FNAME)

        if not regenerate and os.path.exists(processed_skill_path):
            with open(processed_skill_path, 'r+') as f:
                return json.load(f)

        skill_records = self.fetch_raw_skill_list() if skill_records is None else skill_records
        processed_skills = {}

        for skill_record in tqdm.tqdm(skill_records, desc=f"processing {self.skill_list_name} skills"):
            skill_id = skill_record[ID]
            skill_dict = {}

            skill_dict[SKILL_NAME] = skill_record[NAME]
            skill_dict[SKILL_TYPE] = self._get_skill_type(skill_record)

            # clean skill
            skill_dict[SKILL_CLEANED] = self._clean_skill(skill_dict[SKILL_NAME])
            # get len of cleaned name
            skill_dict[SKILL_LEN] = self._count_skill_len(skill_dict[SKILL_CLEANED])

            # get match on stemmed
            skill_dict[MATCH_ON_STEMMED] = self._check_if_match_on_stemmed(skill_dict)

            # infer abbr (in parenthesis AND in list of abbrs)
            skill_dict[ABBREVIATION] = self._get_abbr(skill_record[NAME])

            # stem skill
            skill_dict[SKILL_STEMMED] = self._generate_stemmed_text(skill_dict[SKILL_CLEANED])

            # lemmatize skill
            skill_dict[SKILL_LEMMED] = self._generate_lemmed_text(skill_dict[SKILL_CLEANED])

            processed_skills[skill_id] = skill_dict

        with open(processed_skill_path, "w", encoding='utf-8') as f:
            json.dump(processed_skills, f, ensure_ascii=False, indent=4)

        return processed_skills

    def generate_token_dist_dict(self, regenerate: bool=False,
                                 processed_skill_dict: dict=None,
                                 regenerate_processed_skill_dict: bool=False) -> dict:
        """generate the token distribution dictionary; will regenerate if 1) regenerate is True, or
                2) if the previous intermediate file processed_skill_dict) doesn't exist.
                processed_skill_dict will be used if supplied, otherwise loaded from other methods.
        regenerate_processed_skill_dict is set to False to avoid redundant regeneration in generate_final_skill_list,
        where processed_skill_dict has just been regenerated before this method is called.
        """
        token_dist_path = self.__generate_save_path(TOKEN_DIST_FNAME)

        if not regenerate and os.path.exists(token_dist_path):
            with open(token_dist_path, 'r+') as f:
                return json.load(f)

        processed_skill_dict = self.preprocess_raw_skills(regenerate=regenerate_processed_skill_dict) \
            if processed_skill_dict is None else processed_skill_dict

        long_skill_titles = [processed_skill_dict[key][SKILL_CLEANED]
           for key in processed_skill_dict if processed_skill_dict[key][SKILL_LEN] > 1]
        n_gram_dist = _count_token_dist(long_skill_titles)

        with open(token_dist_path, "w", encoding='utf-8') as f:
            json.dump(n_gram_dist, f, ensure_ascii=False, indent=4)

        return n_gram_dist

    def generate_final_skill_list(self, regenerate: bool=False,
                                  processed_skill_dict: dict=None,
                                  n_gram_dist: dict=None,
                                  ) -> Dict[str, dict]:
        """generate the final skill list; will regenerate if 1) regenerate is True, or
        2) if the previous intermediate files don't exist.
        If processed_skill_dict or processed_skill_dict is supplied, will use them;
        otherwise loaded from other methods"""
        final_skill_path = self.__generate_save_path(FINAL_SKILL_FNAME)

        if not regenerate and os.path.exists(final_skill_path):
            with open(final_skill_path, 'r+') as f:
                return json.load(f)

        # load skill dict and ngram dict from class methods if not specified
        processed_skill_dict = self.preprocess_raw_skills(regenerate=regenerate) \
            if processed_skill_dict is None else processed_skill_dict
        n_gram_dist = self.generate_token_dist_dict(regenerate=regenerate) \
            if n_gram_dist is None else processed_skill_dict

        new_skill_db = {}
        for key in processed_skill_dict:
            self._add_initial_high_low_surfaces_forms(new_skill_db, processed_skill_dict, key, n_gram_dist)

        # TODO to delete?
        # add more surface forms to 2 gram skills (this code section might be deletd in the future )
        list_ = []
        for key in new_skill_db:
            low = new_skill_db[key][LOW_SURFACE_FORMS]
            skill_len = new_skill_db[key][SKILL_LEN]
            if skill_len == 2:
                unique = [l for l in low if len(l.split(' ')) == 1]
                for a in unique:
                    list_.append(a)

        counter = Counter(list_)

        for key in new_skill_db:
            skill_len = new_skill_db[key][SKILL_LEN]
            if skill_len == 2:
                low = new_skill_db[key][LOW_SURFACE_FORMS]
                new_l = []
                for l in low:
                    if len(l.split(' ')) == 1:
                        if counter[l] == 1:
                            new_l.append(l)
                    else:
                        new_l.append(l)
                new_skill_db[key][LOW_SURFACE_FORMS] = new_l

        # search for abbreviation if found 'AQM (Advanced quality management)' -> AQM
        # step 1 extract suspected abv using regex
        # step 2 check if abv is unique in the db (by looking at token dist )

        n_grams = [processed_skill_dict[key] for key in processed_skill_dict
                   if processed_skill_dict[key][SKILL_LEN] > 1]
        rx = r"\b[A-Z](?=([&.]?))(?:\1[A-Z])+\b"

        def extract_sub_forms(skill_name):
            return [x.group() for x in re.finditer(rx, skill_name)]

        def remove_btwn_par(str_):
            return re.sub("[\(\[].*?[\)\]]", "", str_)

        subs = []
        for n_skill in n_grams:
            skill_name = n_skill[SKILL_NAME]
            new_skill_name = remove_btwn_par(skill_name)
            sub_f = extract_sub_forms(new_skill_name)
            if sub_f != []:
                # print(skill_name)
                # print(sub_f)
                # print('--------')
                for s in sub_f:
                    subs.append(s)
        n_gram_dist = Counter(subs)

        for key in new_skill_db:
            if new_skill_db[key][SKILL_LEN] > 2:

                skill_name = new_skill_db[key][SKILL_NAME]
                new_skill_name = remove_btwn_par(skill_name)
                skill_low = new_skill_db[key][LOW_SURFACE_FORMS]
                sub_abv = extract_sub_forms(new_skill_name)
                for abv in sub_abv:
                    if n_gram_dist[abv] == 1:
                        skill_low.append(abv)
                new_skill_db[key][LOW_SURFACE_FORMS] = skill_low

        with open(final_skill_path, "w", encoding='utf-8') as f:
            json.dump(new_skill_db, f, ensure_ascii=False, indent=4)

        return new_skill_db

    def __generate_save_path(self, filename: str) -> str:
        save_dir = os.path.join(FILE_SAVE_PATH, self.skill_list_name)
        os.makedirs(save_dir, exist_ok=True)
        return os.path.join(save_dir, filename)


    def _clean_skill(self, skill_raw_title: str) -> str:
        return re.sub(r'(\(.*\))', '', re.sub(r'[-_/;:.]', ' ',
                                       skill_raw_title)).strip().lower()

    def _get_skill_type(self, skill_record):
        return skill_record[TYPE] if TYPE in skill_record else ""

    def _count_skill_len(self, skill_clean_title: str) -> int:
        return len(skill_clean_title.split(' '))

    def _check_if_match_on_stemmed(self, skill_dict: dict) -> bool:
        return skill_dict[SKILL_LEN] == 1

    def _generate_stemmed_text(self, skill_text) -> str:
        return stem_text(skill_text)

    def _generate_lemmed_text(self, skill_text) -> str:
        return lem_text(skill_text, self.nlp)

    def _add_initial_high_low_surfaces_forms(self, new_skill_db: dict, processed_skill_dict: dict,
                                             skill_key: str, n_gram_dist: dict) -> None:
        high_surface_form = {}
        low_surface_form = []
        match_on_tokens = False
        skill_len = processed_skill_dict[skill_key][SKILL_LEN]
        skill_name = processed_skill_dict[skill_key][SKILL_NAME]
        skill_type = processed_skill_dict[skill_key][SKILL_TYPE]
        clean_name = processed_skill_dict[skill_key][SKILL_CLEANED]
        skill_lemmed = processed_skill_dict[skill_key][SKILL_LEMMED]
        skill_stemmed = processed_skill_dict[skill_key][SKILL_STEMMED]
        abv = processed_skill_dict[skill_key][ABBREVIATION]
        # param diferentiate software and gramatical skills
        uni_match_on_stemmed = processed_skill_dict[skill_key][MATCH_ON_STEMMED]

        # surface forms creation with some relaxation/enrichments
        # to increase proba of matching with natural text

        if abv != '':
            high_surface_form['abv'] = abv
        # unigram skills
        if skill_len == 1:
            high_surface_form['full'] = clean_name
            if uni_match_on_stemmed:
                low_surface_form.append(skill_stemmed)
        # 2-gram skills (ex : project management )
        if skill_len == 2:
            high_surface_form['full'] = skill_lemmed
            # enricj with inverse skills project manag ->  manag project
            stemmed_tokens = skill_stemmed.split(' ')
            inv_stemmed_tokens = stemmed_tokens[::-1]
            low_surface_form.append(skill_stemmed)
            low_surface_form.append(' '.join(inv_stemmed_tokens))
            last = stemmed_tokens[-1]
            start = stemmed_tokens[0]
            # if last token of skill is unique let be identifier of the skill
            # (works well with software where we may choose to use only one term )
            if last in n_gram_dist and n_gram_dist[last] == 1:
                low_surface_form.append(last)

            # TODO to delete?
            # very noisy enrichment (to be deleted)
            """ 
            if dist[start]/dist[last] < RELAX_PARAM:
                low_surface_form.append(start)
            """

        if skill_len > 2:
            high_surface_form['full'] = skill_lemmed
            # if skill with more than 2 tokens the matcher can be on
            # the skill tokens then we agg matches when scoring
            match_on_tokens = True
        # write skill
        new_skill_db[skill_key] = {SKILL_NAME: skill_name,
                             SKILL_TYPE: skill_type,
                             SKILL_LEN: skill_len,
                             HIGH_SURFACE_FORMS: high_surface_form,
                             LOW_SURFACE_FORMS: low_surface_form,
                             MATCH_ON_TOKENS: match_on_tokens
                             }

class EMSISkillProcessor(BaseSkillProcessor):
    """class modified for EMSI"""
    skill_list_name = "EMSI"

    def fetch_raw_skill_list(self) -> List[dict]:
        return fetch_raw_data.fetch_skills_list()

    def _get_skill_type(self, skill_type_data: Any) -> str:
        return skill_type_data[NAME]

    def _get_abbr(self, skill_text) -> str:
        return ""


class EPLSkillProcessor(BaseSkillProcessor):
    """class modified for EmPath Proficiency Library (EPL)"""
    skill_list_name = "EPL"

    def fetch_raw_skill_list(self) -> List[dict]:
        # TODO change this path once we decide where to save the test custom skill list
        with open("../buckets/epl_raw_skills.json", "r+") as f:
            return json.load(f)

    def _get_abbr(self, skill_text) -> str:
        return ""

    def _add_initial_high_low_surfaces_forms(self, new_skill_db: dict, processed_skill_dict: dict,
                                             skill_key: str, n_gram_dist: dict) -> None:
        """for low forms enable "python development" -> add "python" """
        high_surface_form = {}
        low_surface_form = []
        match_on_tokens = False
        skill_len = processed_skill_dict[skill_key][SKILL_LEN]
        skill_name = processed_skill_dict[skill_key][SKILL_NAME]
        skill_type = processed_skill_dict[skill_key][SKILL_TYPE]
        clean_name = processed_skill_dict[skill_key][SKILL_CLEANED]
        skill_lemmed = processed_skill_dict[skill_key][SKILL_LEMMED]
        skill_stemmed = processed_skill_dict[skill_key][SKILL_STEMMED]
        abv = processed_skill_dict[skill_key][ABBREVIATION]
        # param diferentiate software and gramatical skills
        uni_match_on_stemmed = processed_skill_dict[skill_key][MATCH_ON_STEMMED]

        # surface forms creation with some relaxation/enrichments
        # to increase proba of matching with natural text
        if abv != '':
            high_surface_form['abv'] = abv
        # unigram skills
        if skill_len == 1:
            high_surface_form['full'] = clean_name
            if uni_match_on_stemmed:
                low_surface_form.append(skill_stemmed)
        # 2-gram skills (ex : project management )
        if skill_len == 2:
            high_surface_form['full'] = skill_lemmed
            # enricj with inverse skills project manag ->  manag project
            stemmed_tokens = skill_stemmed.split(' ')
            inv_stemmed_tokens = stemmed_tokens[::-1]
            low_surface_form.append(skill_stemmed)
            low_surface_form.append(' '.join(inv_stemmed_tokens))
            last = stemmed_tokens[-1]
            start = stemmed_tokens[0]
            # if last token of skill is unique let be identifier of the skill
            # (works well with software where we may choose to use only one term )
            if last in n_gram_dist and n_gram_dist[last] == 1:
                low_surface_form.append(last)

            # "python development" -> add "python"
            if start in n_gram_dist and n_gram_dist[start] == 1:
                low_surface_form.append(start)

        if skill_len > 2:
            high_surface_form['full'] = skill_lemmed
            # if skill with more than 2 tokens the matcher can be on
            # the skill tokens then we agg matches when scoring
            match_on_tokens = True
        # write skill
        new_skill_db[skill_key] = {SKILL_NAME: skill_name,
                                   SKILL_TYPE: skill_type,
                                   SKILL_LEN: skill_len,
                                   HIGH_SURFACE_FORMS: high_surface_form,
                                   LOW_SURFACE_FORMS: low_surface_form,
                                   MATCH_ON_TOKENS: match_on_tokens
                                   }


if __name__ == "__main__":
    from spacy.matcher import PhraseMatcher
    import json

    from skillNer.skill_extractor_class import SkillExtractor

    # instantiate processor based on the skill list to use
    esp = EPLSkillProcessor()
    skill_processed = esp.generate_final_skill_list()

    # init params of skill extractor
    nlp = en_core_web_lg.load()

    # init skill extractor
    skill_extractor = SkillExtractor(nlp, skill_processed, PhraseMatcher)

    # extract skills from job_description
    job_description = """
     have experience with Python. and have the initiative to take ownership. 
     familiarity with REST framework. experience implementing APIs. 
     Familiar with Agile Development. Experience with Web Development. 
     Comfortable working in a team.
     """

    annotations = skill_extractor.annotate(job_description)
