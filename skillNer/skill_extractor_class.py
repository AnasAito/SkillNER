# native packs
#
# installed packs
from spacy import displacy
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

    def annotate(
        self,
        text: str
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

        # process filter
        n_gram_pro = self.utils.process_n_gram(skills_ngram, text_obj)
        uni_gram_pro = self.utils.process_unigram(skills_uni, text_obj)

        return {'text': text_obj.transformed_text,
                'results': {
                    'full_match': skills_full,
                    'ngram_full_match': skills_sub_full,
                    'ngram_scored': n_gram_pro,
                    'unigram_scored': uni_gram_pro
                }}

    def display(self, results):

        text = results['text']
        skill_extractor_results = results['results']
        ents = []
        matches = []
        colors_id = []
        colors = {}
        tokens = text.split(' ')
        skill_to_color = {'Hard Skill': '#818CF8', 'Soft Skill': '#F472B6'}

        for match_type in skill_extractor_results.keys():
            for match in skill_extractor_results[match_type]:
                matches .append(match)

        for match in matches:
            entity = {}
            start = sum(
                [len(token)+1 for token in tokens[:match['doc_node_id'][0]]])

            entity['start'] = start

            end = start+sum(
                [len(token)+1 for token in tokens[match['doc_node_id'][0]:1+match['doc_node_id'][-1]]])

            entity['end'] = end
            entity['label'] = self.skills_db[match['skill_id']]['skill_name']
            colors[entity['label']
                   ] = skill_to_color[self.skills_db[match['skill_id']]['skill_type']]
            colors_id.append(entity['label'])
            ents.append(entity)
        ents.sort(key=lambda x: x['start'], reverse=False)
        ex = [{"text": text,
               "ents": ents,
               "title": None}]

        options = {"ents": colors_id, "colors": colors}
        html = displacy.render(ex, style="ent", manual=True, options=options)
