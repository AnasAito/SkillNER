<section align="center">

# ``skillner``

## A smart rule based NLP module to extract skills from text

[**Live demo**](https://share.streamlit.io/anasaito/skillner_demo/index.py) | [**Documentation**](https://anasaito.github.io/SkillNER/index.html) | [**Website**](https://skillner.vercel.app/)
</section>

![build](https://github.com/AnasAito/skillner/workflows/tests/badge.svg)
[![Downloads](https://static.pepy.tech/personalized-badge/skillner?period=month&units=international_system&left_color=blue&right_color=green&left_text=Downloads%20/%20months)](https://pepy.tech/project/skillner)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI version](https://badge.fury.io/py/skillner.svg)


## Quick start

Run the following command to get the latest version ``skillner``
```bash
pip install skillner -U
```

Download the english skills knowledge base
```bash
skillner-download ESCO_EN
```


## Development 

1. Start by forking the repository
2. Clone the repository and ``cd`` to it
```bash
git clone https://github.com/{YOUR_GITHUB_USERNAME}/SkillNER.git
cd SkillNER
```
3. Install the package in development mode
```bash
pip install -e .[dev]
```
Et voilà *you're ready to hit the ground running*!

To build the documentation, run the followings
```bash
cd doc
make html
```