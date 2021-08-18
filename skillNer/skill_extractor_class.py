# native packs
#
# installed packs
from spacy import displacy
# my packs
from skillNer.text_class import Text
from skillNer.matcher_class import Matchers, SkillsGetter
from skillNer.utils import Utils
from skillNer.general_params import SKILL_TO_COLOR


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

    def annotate(
        self,
        text: str,
        tresh: float = 0.5,debug=False
    ):

        # create text object
        text_obj = Text(text, self.nlp)

        # match text
        skills_full, text_obj = self.skill_getters.get_full_match_skills(
            text_obj, self.matchers['full_matcher'])
        skills_sub_full, skills_ngram, text_obj = self.skill_getters.get_sub_match_skills(
            text_obj, self.matchers['ngram_matcher'])
        skills_uni = self.skill_getters.get_single_match_skills(
            text_obj, self.matchers['uni_gram_matcher'])
        skills_abv = self.skill_getters.get_abv_match_skills(
            text_obj, self.matchers['abv_matcher'])
        #skills_ut = self.skill_getters.get_abv_match_skills(
        #    text_obj, self.matchers['ut_matcher'])    
        
        # process uni_match
        uni_gram_pro =  self.utils.process_unigram(skills_uni, text_obj)
        unigram_full = [match for match in uni_gram_pro if match['score']==1]
        unigram_sub = [match for match in uni_gram_pro if (match['score']>=tresh and match['score']<1) ]
        ## prepare full matches ids  for submatch context scoring 
        # get full match ids 
        full_sk = skills_full+skills_sub_full+skills_abv+unigram_full#+skills_ut
        full_matches_ids = [match['skill_id'] for match in full_sk ]
        # get high confid unigram ids 
        uni_matches_ids = [match['skill_id'] for match in unigram_full ]
        
        # process ngram
        # full_ids 
        full_ids = full_matches_ids + uni_matches_ids 
        n_gram_scored = self.utils.process_n_gram(skills_ngram, text_obj , full_matches_ids =full_ids )
        n_gram_pro = [skill_match for skill_match in n_gram_scored if skill_match['score'] >= tresh]

        if debug : 
             return {
                 'text': text_obj.transformed_text,
                 'results': {
                     'full_matches': full_sk ,
                     'ngram_scored': n_gram_pro,
                     'unigram_scored': unigram_sub,
                 },
                 'logs': {'full_match':skills_full ,
                           'full_ngram':skills_sub_full,
                           'abrv_match' :skills_abv,
                           #'ut_full':skills_ut ,
                           'unigrqm_full' : unigram_full , 
                           'ngram_scored': n_gram_scored,
                           'unigram_scored': [match for match in uni_gram_pro if  match['score']<1 ], 
                         }
             }
        else : 
             return {
                 'text': text_obj.transformed_text,
                 'results': {
                     'full_matches': full_sk ,
                     'ngram_scored': n_gram_pro,
                     'unigram_scored': unigram_sub,
                 }}

    def display(
        self,
        results
    ):

        # explode result object
        text = results["text"]
        skill_extractor_results = results['results']

        # words and their positions
        words_position = Text.words_start_end_position(text)

        # get matches
        matches = []
        for match_type in skill_extractor_results.keys():
            for match in skill_extractor_results[match_type]:
                matches.append(match)

        # displacy render params
        entities = []
        colors = {}
        colors_id = []

        # fill params
        for match in matches:
            # skill id
            skill_id = match["skill_id"]

            # index of words in skill
            index_start_word, index_end_word = match['doc_node_id'][0], match['doc_node_id'][-1]

            # build/append entity
            entity = {
                "start": words_position[index_start_word].start,
                "end": words_position[index_end_word].end,
                "label": self.skills_db[skill_id]['skill_name']
            }
            entities.append(entity)

            # highlight matched skills
            colors[entity['label']
                   ] = SKILL_TO_COLOR[self.skills_db[skill_id]['skill_type']]
            colors_id.append(entity['label'])

        # prepare params
        entities.sort(key=lambda x: x['start'], reverse=False)
        options = {"ents": colors_id, "colors": colors}
        ex = {
            "text": text,
            "ents": entities,
            "title": None
        }

        # render
        html = displacy.render(ex, style="ent", manual=True, options=options)
