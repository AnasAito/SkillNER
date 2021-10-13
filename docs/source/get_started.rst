Getting started
===============

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id molestie lorem. 
Aliquam dignissim felis id dolor bibendum, et viverra nisl tincidunt. 
Mauris at neque nunc. 


Installation
------------

skillNer can be installed through the *python package-manager* pip by runing the command
::

  $ pip install skillNer


Quickstart
----------

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id molestie lorem. 
Aliquam dignissim felis id dolor bibendum, et viverra nisl tincidunt. 
Mauris at neque nunc. 


.. code:: python

    # imports
    import spacy
    from spacy.matcher import PhraseMatcher

    # load default skills data base
    from skillNer.general_params import SKILL_DB
    # import skill extractor
    from skillNer.skill_extractor_class import SkillExtractor

    # init params of skill extractor
    nlp = spacy.load("en_core_web_lg")
    stop_words = set(stopwords.words('english'))

    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

    # extract skills from job_description
    job_description = """
    You are a Python Developer with a solid experience in Web development and  esx
    and have a thoughtful expatriation and manage project . You're passionate and powerful.
    You are recognized for your ability to evolve within a team and around common projects
    and you easily adapt in a new environment. javascript and node and french and english
    """

    annotations = skill_extractor.annotate(job_description)


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id molestie lorem. 
Aliquam dignissim felis id dolor bibendum, et viverra nisl tincidunt. 
Mauris at neque nunc. 