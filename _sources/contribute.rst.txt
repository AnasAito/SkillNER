Contribute
==========


Why and How to contribute?
-----------------------------------------

SkillNer is the first **Open Source** skill extractor. 
Hence it is a tool dedicated to the community and thereby relies on its contribution to evolve.

We did our best to adapt SkillNer for usage and fixed many of its bugs. Therefore, we believe its key features 
make it ready for a diversity of use cases.
However, it still has not reached 100% stability. SkillNer need the assistance of the community to be adapted further
and broaden its usage. 


You can contribute to SkillNer either by

- Reporting issues. Indeed, you may encounter one while you are using SkillNer. So do not hesitate to mention them in the `issue section of our GitHub repository <https://github.com/AnasAito/SkillNER/issues>`_. Also, you can use the issue as a way to suggest new features to be added.

- Pushing code to our repository through pull requests. In case you fixed an issue or wanted to extend SkillNer features.


A third (friendly) option to contribute to SkillNer will be soon released. *So, stay tuned...*


.. note::
    Make sure to follow the guidelines below when contributing. This is in order to ensure commune standards of contribution.
    By following them, we and others could get what you want to say.



Setup the project on your local machine
---------------------------------------

Cloning the repository
~~~~~~~~~~~~~~~~~~~~~~

The first thing to do is to create a folder (name it whatever you want) ``cd`` to it.
Within that folder, clone SkillNer repository by running

::

  $ git clone https://github.com/AnasAito/SkillNER.git


Afterward, ``cd`` to SkillNer folder


Setup the environment
~~~~~~~~~~~~~~~~~~~~~

Here, we will create a ``conda environment``. All the dependencies of the SkillNer are mentioned in ``environment.yml`` file. 
Lauch you Anaconda prompt and cd to SkillNer folder that you have just cloned, then run the following command

::

  $ conda env create -f environment.yml


We are almost done, in a notebook cell run the following command to install ``spacy en_core_web_sm`` 
or run the sandbox notebook (this notebook comes with SkillNer repo)


::

  !python -m spacy download en_core_web_sm


.. note::
    You can set up the environment through the classic way by creating a ``virtual environment`` and running 
    ::

      $ pip install -r requirements.txt
    
    However, you need to install additional packages to be able to use the python interpreter in a Jupyter notebook.



Some general guidelines
-----------------------

To contribute, make sure to follow these guidelines.


Report an issue
~~~~~~~~~~~~~~~

When reporting an issue, try to be as much clear as possible. Describe the issue and the expected behavior. 
Provide us with the (buggy) code snippets so that we can reproduce the issue.


Pull request
~~~~~~~~~~~~

In the description of the pull request, mention its purpose (fix bug, add features, code enhancement, ...).

If you are willing to push code to SkillNer, make sure to document it through docstrings. 
Also, add comments to your code to explain what it does.

This will help us revue your contribution.
