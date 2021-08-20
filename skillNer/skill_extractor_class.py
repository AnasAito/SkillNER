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
                # get matches
        skills_full, text_obj = self.skill_getters.get_full_match_skills(
            text_obj, self.matchers['full_matcher'])
        
        skills_abv , text_obj = self.skill_getters.get_abv_match_skills(
            text_obj, self.matchers['abv_matcher'])
        
        skills_uni_full, text_obj = self.skill_getters.get_full_uni_match_skills(
            text_obj, self.matchers['full_uni_matcher'])
        
        skills_low_form,text_obj =self.skill_getters.get_low_match_skills(
            text_obj, self.matchers['low_form_matcher'])
        
        skills_on_token =self.skill_getters.get_token_match_skills(
            text_obj, self.matchers['token_matcher'])
        full_sk = skills_full + skills_abv
              ## process uni_token conflicts  
        to_process = skills_on_token + skills_low_form + skills_uni_full
        process_n_gram = self.utils.process_n_gram(to_process, text_obj  )
        
            
        


        
        
        
        
        
        return {
                 'text': text_obj.transformed_text,
                 'results': {
                     'full_matches': full_sk ,
                     'ngram_scored': [match for match in process_n_gram if match['score']>=tresh],
                   
                             }
               }
    



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
