.. _dev:

Development
===========

1. Start by forking the repository

2. Clone the repository and ``cd`` to it

.. code-block:: bash

    $ git clone https://github.com/{YOUR_GITHUB_USERNAME}/SkillNER.git
    $ cd SkillNER


3. Install the package in development mode

.. code-block:: bash

    $ pip install -e .[dev]

Et voilà *you're ready to hit the ground running*!

To build the documentation, run the followings

.. code-block:: bash

    $ cd doc
    $ make html
