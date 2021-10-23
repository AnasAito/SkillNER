# native packs
#
# installed packs
from spacy import displacy
# my packs
from skillNer.text_class import Text
from skillNer.matcher_class import Matchers, SkillsGetter
from skillNer.utils import Utils
from skillNer.general_params import SKILL_TO_COLOR

from skillNer.visualizer.html_elements import DOM, render_phrase
from skillNer.visualizer.phrase_class import Phrase


class SkillExtractor:
    """Main class to annotate skills in a given text and visualize them.
    """

    def __init__(
        self,
        nlp,
        skills_db,
        phraseMatcher,
        tranlsator_func=False
    ):
        """Constructor of the class.

        Parameters
        ----------
        nlp : [type]
            NLP object loaded from spacy.
        skills_db : [type]
            A skill database used as a lookup table to annotate skills.
        phraseMatcher : [type]
            A phrasematcher loaded from spacy.
        tranlsator_func :Callable
            A fucntion to translate text from source language to english def tranlsator_func(text_input: str) -> text_input:str
        """

        # params
        self.tranlsator_func = tranlsator_func
        self.nlp = nlp
        self.skills_db = skills_db
        self.phraseMatcher = phraseMatcher

        # load matchers: all
        self.matchers = Matchers(
            self.nlp,
            self.skills_db,
            self.phraseMatcher,
            # self.stop_words
        ).load_matchers()

        # init skill getters
        self.skill_getters = SkillsGetter(self.nlp)

        # init utils
        self.utils = Utils(self.nlp, self.skills_db)
        return

    def annotate(
        self,
        text: str,
        tresh: float = 0.5
    ) -> dict:
        """To annotate a given text and thereby extract skills from it.

        Parameters
        ----------
        text : str
            The target text.
        tresh : float, optional
            A treshold used to select skills in case of confusion, by default 0.5

        Returns
        -------
        dict
            returns a dictionnary with the text that was used and the annotated skills (see example).

        Examples
        --------
        >>> import spacy
        >>> from spacy.matcher import PhraseMatcher
        >>> from skillNer.skill_extractor_class import SkillExtractor
        >>> from skillNer.general_params import SKILL_DB
        >>> nlp = spacy.load('en_core_web_sm')
        >>> skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
        loading full_matcher ...
        loading abv_matcher ...
        loading full_uni_matcher ...
        loading low_form_matcher ...
        loading token_matcher ...
        >>> text = "Fluency in both english and french is mandatory"
        >>> skill_extractor.annotate(text)
        {'text': 'fluency in both english and french is mandatory',
        'results': {'full_matches': [],
        'ngram_scored': [{'skill_id': 'KS123K75YYK8VGH90NCS',
            'doc_node_id': [3],
            'doc_node_value': 'english',
            'type': 'lowSurf',
            'score': 1,
            'len': 1},
        {'skill_id': 'KS1243976G466GV63ZBY',
            'doc_node_id': [5],
            'doc_node_value': 'french',
            'type': 'lowSurf',
            'score': 1,
            'len': 1}]}}
        """

        # check translator
        if self.tranlsator_func:
            text = self.tranlsator_func(text)

        # create text object
        text_obj = Text(text, self.nlp)
        # get matches
        skills_full, text_obj = self.skill_getters.get_full_match_skills(
            text_obj, self.matchers['full_matcher'])

        # tests

        skills_abv, text_obj = self.skill_getters.get_abv_match_skills(
            text_obj, self.matchers['abv_matcher'])

        skills_uni_full, text_obj = self.skill_getters.get_full_uni_match_skills(
            text_obj, self.matchers['full_uni_matcher'])

        skills_low_form, text_obj = self.skill_getters.get_low_match_skills(
            text_obj, self.matchers['low_form_matcher'])

        skills_on_token = self.skill_getters.get_token_match_skills(
            text_obj, self.matchers['token_matcher'])
        full_sk = skills_full + skills_abv
        # process pseudo submatchers output conflicts
        to_process = skills_on_token + skills_low_form + skills_uni_full
        process_n_gram = self.utils.process_n_gram(to_process, text_obj)

        return {
            'text': text_obj.transformed_text,
            'results': {
                'full_matches': full_sk,
                'ngram_scored': [match for match in process_n_gram if match['score'] >= tresh],

            }
        }

    def display(
        self,
        results: dict
    ):
        """To display the annotated skills. 
        This method uses built-in classes of spacy to render annotated text, namely `displacy`.

        Parameters
        ----------
        results : dict
            results is the dictionnary resulting from applying `.annotate()` to a text.

        Results
        -------
        None 
            render the text with annotated skills.
        """

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

    def describe(
        self,
        annotations: dict
    ):
        """To display more details about the annotated skills.
        This method uses HTML, CSS, JavaScript combined with IPython to render the annotated skills.

        Parameters
        ----------
        annotations : dict
            annotations is the dictionnary resulting from applying `.annotate()` to a text.

        Returns
        -------
        [type]
            render text with annotated skills.
        """

        # build phrases to display from annotations
        arr_phrases = Phrase.split_text_to_phare(
            annotations,
            self.skills_db
        )

        # create DOM
        document = DOM(children=[
            render_phrase(phrase)
            for phrase in arr_phrases
        ])

        # render
        return document
