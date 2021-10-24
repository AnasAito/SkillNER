Getting started
===============

It is easy to get started with **SkillNer** and take advantage of its features. 
This starter guide will walk you through the steps to follow 
and will provide you with small snippets to get started.



Installation
------------

SkillNer can be installed through the *python package-manager* pip by running the command
::

  $ pip install skillNer


Also, you need to download ``spacy en_core_web_sm``. We will need it to initialize an NLP object that will
be plugged into SkillNer. To do so, run the following command:   

::

  $ python -m spacy download en_core_web_sm


.. note::

    Thanks to its modular nature, you can customize the behavior of SkillNer just 
    by tuning | pluging | unpluging modules. Don't worry about that, we will get into it later! 



Quickstart
---------

With these initial steps being accomplished, 
let's dive a bit deeper into SkillNer through a worked example.


Let's say you want to extract skills from the following job posting:
*"You are a Python developer with a solid experience in web development
and can manage projects. You quickly adapt to new environments 
and speak fluently English and French"*


 
1. We start first by importing modules, particularly spacy and SkillExtractor. 
Note that if you are using SkillNer for the first time, it might take a while to download **SKILL_DB**.

**SKILL_DB** is SkillNer default skills database. It was built upon `EMSI skills database <https://skills.emsidata.com/>`_.

.. code:: python

    # imports
    import spacy
    from spacy.matcher import PhraseMatcher

    # load default skills data base
    from skillNer.general_params import SKILL_DB
    # import skill extractor
    from skillNer.skill_extractor_class import SkillExtractor


2. Next, we load NLP object from `spacy <https://spacy.io/>`_. Afterward, we initialize an instance of SkillExtractor.

.. code:: python

    # init params of skill extractor
    nlp = spacy.load("en_core_web_sm")
    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


3. Lastly, we call the ``.annotate`` method of the instantiated object to annotate skill within the job description.

.. code:: python

    # extract skills from job_description
    job_description = """
    You are a Python developer with a solid experience in web development
    and can manage projects. You quickly adapt to new environments 
    and speak fluently English and French
    """

    annotations = skill_extractor.annotate(job_description)


Voilà! Now you can inspect skills by rendering the text with the annotated skills.
This can be achieved by calling the method ``.describe``.

.. code:: python

    # to inspect annotations
    skill_extractor.describe(annotations)


.. raw:: html
   :file: describe.html


.. note::

    The output of ``.describe`` method is literally an HTML document that is rendered in the notebook cell.



What's next?
-----------

The above snippets show a basic example of a SkillNer use case.
By simply being able to extract skills from text, SkillNer opens thousands of other application
from describing the market labor to constructing knowledge graphs.

For further readings, check the :ref:`tutorials` section. 
