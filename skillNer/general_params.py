# native packs
import os
import json
from posixpath import dirname
# installed packs
#
# my packs
from skillNer.network.remote_db import RemoteBucket

# mapping skill and color
SKILL_TO_COLOR = {
    'Hard Skill': '#818CF8',
    'Soft Skill': '#F472B6',
    'Certification': "#552448"
}

# mapping skill and color tail
SKILL_TO_COLOR_TAILWIND = {
    'Hard Skill': 'red-500',
    'Soft Skill': 'blue-500',
    'Certification': "green-500"
}


# init remote bucket to fetch db in case they don't exist locally
bucket = RemoteBucket(
    branch="first_release"
)

# load local data
# else fetch remote data and save it
try:
    with open('skill_db_relax_20.json') as json_file:
        SKILL_DB = json.load(json_file)
except:
    SKILL_DB = bucket.fetch_remote("SKILL_DB")
    # dump data
    with open('skill_db_relax_20.json', 'w') as fp:
        json.dump(SKILL_DB, fp)

# load token distribution dict
try:
    with open('token_dist.json') as json_file:
        TOKEN_DIST = json.load(json_file)
except:
    TOKEN_DIST = bucket.fetch_remote("TOKEN_DIST")
    # dump data
    with open('token_dist.json', 'w') as fp:
        json.dump(TOKEN_DIST, fp)


# list of punctuation
LIST_PUNCTUATIONS = ['/', '·', ',', '.',
                     '-', '(', ')', ',', ':', '!', "'", '?']

# list of redundant words to remove from text
S_GRAM_REDUNDANT = [
    'no no',
    'of the',
    'you have',
    'in the',
    'experience in',
    'ability to',
    'knowledge of',
    'pdf format',
    'at least',
    'experience of',
    'you are',
    'mastery of',
    'to the',
    'least years',
    'years of',
    'sense of',
    'years in',
    'or equivalent',
    'of at',
    'professional experience',
    'the field',
    'in similar',
    'copy of',
    'field of',
    'of experience',
    'similar position',
    'on the',
    'ofppt ma',
    'level of',
    'in pdf',
    'to justify',
    'will be',
    'good knowledge',
    'to be',
    'of years',
    'you justify',
    'justify cumulative',
    'an asset',
    'degree in',
    'cumulative professional',
    'access to',
    'in computer',
    'to work',
    'have good',
    'how to',
    'for the',
    'related to',
    'to hold',
    'the position',
    'an experience',
    'able to',
    'very good',
    'mastering the',
    'diploma giving',
    'the public',
    'giving access',
    'public service',
    'training in',
    'must be',
    'diploma diploma',
    'you re',
    'and you',
    'required diploma',
    'is an',
    'by foreign',
    'foreign institutions',
    'institutions must',
    'accompanied by',
    'copies of',
    'of certificates',
    'certificates of',
    'of equivalence',
    'recto verso',
    'downloadable from',
    'www ofppt',
    'experience related',
    'the required',
    'be accompanied',
    'by copies',
    'application form',
    'the cni',
    'cni recto',
    'issued by',
    'equivalence pdf',
    'verso in',
    'format one',
    'one page',
    'page only',
    'diploma issued',
    'and or',
    'position pdf',
    'bac training',
    'the job',
    'computer science',
    'format downloadable',
    'updated cv',
    'from www',
    'detailing the',
    'team spirit',
    'for information',
    'cv detailing',
    'job experience',
    'technician or',
    'have an',
    'information pdf',
    'spirit of',
    'would be',
    'than that',
    'oral and',
    'and written',
    'and oral',
    'years experience',
    'good level',
    'of moroccan',
    'be considered',
    'or more',
    'the following',
    'the application',
    'of age',
    'the offer',
    'or similar',
    'of applications',
    'the date',
    'date of',
    'moroccan nationality',
    'minimum experience',
    'and apply',
    'an application',
    'form f1',
    'other than',
    'will not',
    'not be',
    'candidature file',
    'to submit',
    'submit an',
    'by sending',
    'deadline for',
    'for receipt',
    'receipt of',
    'applications is',
    '2021 at',
    'at midnight',
    'bac in',
    'with the',
    'transmitted via',
    'via channel',
    'channel other',
    'that mentioned',
    'mentioned above',
    'above will',
    'analysis and',
    'you to',
    'register and',
    'sending the',
    'application file',
    'file in',
    'the website',
    'minimum of',
    'experience as',
    'know how',
    'http recruitment',
    'recruitment ofppt',
    'format to',
    'website http',
    'perfect mastery',
    'bachelor degree',
    'age on',
    'f1 for',
    'have the',
    'any file',
    'higher education',
    'command of',
    'file transmitted',
    'technical skills',
    'good relationship',
    'entry into',
    'into service',
    'engineering school',
    'of entry',
    'an excellent',
    'this position',
    'knowledge in',
    'of service',
    'good mastery',
    'scale of',
    'july 2021',
    'and the',
    'of analysis',
    'you master',
    'equivalent in',
    'have at',
    'writing and',
    'want to',
    'as team',
    'what you',
    'first experience',
    'technical expertise',
    'training bac',
    'is that',
    'that what',
    're saying',
    'master degree',
    'to manage',
    'to years',
    'at the',
    'years as',
    'offer you',
    'is plus',
    'a good',
    'fluency in'
]
