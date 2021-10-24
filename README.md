<p align="center"><img width="50%" src="https://user-images.githubusercontent.com/56308112/128958594-79813e72-b688-4a9a-9267-324f098d4b0c.png" /></p>


SkillNer is a NLP module to automatically Extract skills and certifications from unstructured job postings, texts and applicant's resumes.

In particular, there is a custom tokenizer that adds tokenization rules on top of spaCy's
rule-based tokenizer, a POS tagger and syntactic parser trained on biomedical data and
an entity span detection model. Separately, there are also NER models for more specific tasks.

**Just looking to test out SkillNer? Check out our [demo](https://share.streamlit.io/anasaito/skillner_demo/index.py)**.


## Installation
Installing scispacy requires two steps: installing spacy and one of its models  then  install the library, run:
```bash
pip install spacy 
```

to install a model (see our full selection of available models below), run a command like the following:

```bash
python -m spacy download en_core_web_sm
```
Finalluy install skillNer
```bash
pip install skillner 
```

## Example Usage

With these initial steps being accomplished, let’s dive a bit deeper into skillNer through a worked example.

Let’s say you want to extract skills from the following job posting: “You are a Python developer with a solid experience in web development and can manage projects. You quickly adapt to a new environment and speak fluently English and French”

1. We start first by importing modules, particularly spacy and SkillExtractor. Note that if you are using skillNer for the first time, it might take a while to download SKILL_DB.

SKILL_DB is skillNer default skills database. It was built upon EMSI skills database (link).

```python
# imports
import spacy
from spacy.matcher import PhraseMatcher

# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

# init params of skill extractor
nlp = spacy.load("en_core_web_sm")
# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# extract skills from job_description
job_description = """
You are a Python developer with a solid experience in web development
and can manage projects. You quickly adapt to a new environment
and speak fluently English and French
"""

annotations = skill_extractor.annotate(job_description)


```


### skillner display




## Citing




