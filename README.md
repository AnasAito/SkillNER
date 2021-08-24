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
job_description = """
You are a Python Developer with a solid experience in Web development and  esx
and have a thoughtful expatriation and manage project . You're passionate and powerful.
You are recognized for your ability to evolve within a team and around common projects
and you easily adapt in a new environment. javascript and node and french and english
"""

annotations = skill_extractor.annotate(job_description)
# # output:
# {
#  'text': "original text"
#  'results': {'full_matches': [
#                         {
#                             'doc_node_id': [11],
#                             'doc_node_value': 'node',
#                             'score': 0.9
#                         }, ...
#                 ],
#              'ngram_scored': [...],
#              'unigram_scored': [...]
#         }
# }
```

- Here is how you can show the results of the annotation in a compact way
```python
skill_extractor.display(annotations)
# ouput:
# text annotated using scapcy displacy 
# (see screenshot below)
```

<img src="screenshots/annotated_text.png" alt="output of skill_extractor.display(annotations)">


- Here is how to show more details about the annoation, also in compact way

```python
skill_extractor.display_details(annotations)
# text annoated using using pure HTML CSS and Javascript 
# see animation below
```

<img src="screenshots/gif_visualizer.gif" alt="animation of skill_extractor.display_details(annotations)">


##  Todos :
- create skill graph (using real data ) for new sub_matches scorer 
- rewrite ngram and unigram scorer using ccontext scorer 
