import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = [
    "numpy",
    "pandas",
    "nltk",
    "spacy",
]

setuptools.setup(
    name="skillNer",
    version="0.0.2",
    author="Anas Ait AOMAR / Badr MOUFAD",
    author_email="pedroslashs@gmail.com",
    description="A first deployed version of skillNer",
    long_description=long_description,
    url="https://github.com/AnasAito/SkillNER",
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    package_data={'': ['skillNer/skills_processed.json']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::  :: No license",
        "Operating System :: OS Independent",
    ],
)
