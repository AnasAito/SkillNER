# SkillNER project

## Project overview : 
- The goal of this project is to build a named entity extraction solution for skill extraction from job posting text.
- Our solution merges a rule-based matcher that labels data and feeds it. to aBERT model that we will fine-tune for skills recognition.

![image](https://user-images.githubusercontent.com/56308112/128958594-79813e72-b688-4a9a-9267-324f098d4b0c.png)


## Documentation : 
Visit this [notion link](https://sudsy-dill-008.notion.site/f6596c10b49545d5a740e0ecc21a5a46?v=801ba1af94a0484d8af732347c211fb0) for updated documentation about the project 


## Collaborations 
- I add weekly new issues regarding skill extractor, choose an issue and lest start a conversation to fix it 
- If you wanna jump to code open notebooks/skills-extractor that contain all modules used to extract skills 

## install SkillNER
Since **SkillNER** is still a private project, only the contributors are allowed to pip install it. To install **SkillNER** in your project and use it, here are capstone steps to follow:

1. You need to generate a **personal token**. You can achieve that by following [these steps](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)
Only tick **repo** to give reading / writing access to your repos


2. To install **SkillNER**, hit the following command,


`pip install git+https://{YOUR_GENERATED_TOKEN}@github.com/AnasAito/SkillNER.git`


in my case this command looks like that:


`pip install git+https://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@github.com/AnasAito/SkillNER.git`


**Note** that for privacy and security reasons, I re-updated this token. Hence, it is no longer valid to pip install **SkillNER**.


3. Here is a snippets to get started with **SkillNER**:

```python
# imports
import spacy
from spacy.matcher import PhraseMatcher
from nltk.corpus import stopwords

# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor


# init params of skill extractor
nlp = spacy.load("en_core_web_lg")
stop_words = set(stopwords.words('english'))

# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher, stop_words)

# extract skills from job_description
job_description = "We need an expert in esport management. Fluency in both english and french is mandatory!"

annotations = skill_extractor.annotate(input_)
# # output:
{'logs': {'abrv_match': [{'doc_node_id': [10],
                          'doc_node_value': 'css',
                          'score': 1,
                          'skill_id': 'KS121F45VPV8C9W3QFYH'}],
          'full_match': [],
          'full_ngram': [{'doc_node_id': [5, 6],
                          'score': 1,
                          'skill_id': 'ES8AAD06BE8119038221'}],
          'ngram_scored': [{'doc_node_id': [1],
                            'doc_node_value': 'need',
                            'score': 0.49,
                            'skill_id': 'ESEE2FE3695A215DC6DC'},
                           {'doc_node_id': [3],
                            'doc_node_value': 'expert',
                            'score': 0.5,
                            'skill_id': 'KS123RD5VV5WNJLMNH3J'},
                           {'doc_node_id': [10],
                            'doc_node_value': 'css',
                            'score': 0.46,
                            'skill_id': 'KS122KN6KY17NGPWFDVB'},
                           {'doc_node_id': [11],
                            'doc_node_value': 'node',
                            'score': 0.3,
                            'skill_id': 'KS1272978ZVDGYKBS082'},
                           {'doc_node_id': [12],
                            'doc_node_value': 'english',
                            'score': 0.6,
                            'skill_id': 'KS123K75YYK8VGH90NCS'},
                           {'doc_node_id': [14],
                            'doc_node_value': 'french',
                            'score': 0.6,
                            'skill_id': 'KS1243976G466GV63ZBY'}],
          'unigram_scored': [{'doc_node_id': [11],
                              'doc_node_value': 'node',
                              'score': 0.9,
                              'skill_id': 'KS126ZK60X10ZQ7DRFLR'}],
          'unigrqm_full': []},
 'results': {'full_matches': [{'doc_node_id': [5, 6],
                               'score': 1,
                               'skill_id': 'ES8AAD06BE8119038221'},
                              {'doc_node_id': [10],
                               'doc_node_value': 'css',
                               'score': 1,
                               'skill_id': 'KS121F45VPV8C9W3QFYH'}],
             'ngram_scored': [{'doc_node_id': [3],
                               'doc_node_value': 'expert',
                               'score': 0.5,
                               'skill_id': 'KS123RD5VV5WNJLMNH3J'},
                              {'doc_node_id': [12],
                               'doc_node_value': 'english',
                               'score': 0.6,
                               'skill_id': 'KS123K75YYK8VGH90NCS'},
                              {'doc_node_id': [14],
                               'doc_node_value': 'french',
                               'score': 0.6,
                               'skill_id': 'KS1243976G466GV63ZBY'}],
             'unigram_scored': [{'doc_node_id': [11],
                                 'doc_node_value': 'node',
                                 'score': 0.9,
                                 'skill_id': 'KS126ZK60X10ZQ7DRFLR'}]},
 'text': 'we need an expert in esport management fluency in both css node '
         'english and french is mandatory'}

skill_extractor.display(annotations)
# ouput:
# text annotated using scapcy displacy (see screenshot below)
```

<img src="screenshots/displacy_result.png" alt="output of skill_extractor.display(annotations)">


##  Todos :
- create skill graph (using real data ) for new sub_matches scorer 
- rewrite ngram and unigram scorer using ccontext scorer 
