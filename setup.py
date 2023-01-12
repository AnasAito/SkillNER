import setuptools


dependencies = [
    "numpy",
    "pandas",
    "nltk",
    "spacy",
    "jellyfish",
    "ipython",
    "scipy"
]

setuptools.setup(
    name="skillNer",
    version="1.0.3",
    author="Anas Ait AOMAR & Badr MOUFAD",
    author_email="Badr.MOUFAD@emines.um6p.ma",
    description="An NLP module to automatically Extract skills and certifications from unstructured job postings, texts, and applicant's resumes",
    url="https://github.com/AnasAito/SkillNER",
    keywords=["skillNer", 'python', 'NLP', "NER",
              "skills-extraction", "job-description"],
    download_url='https://github.com/AnasAito/SkillNER/archive/refs/tags/v1.0.3.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
)
