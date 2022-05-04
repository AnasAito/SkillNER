# Skill db prep pipeline 
## 1. create skills_processed.json
- generate **skill_name** : raw skill label 
- generate **skill_type** : skill type if found in db 
- generate **skill_cleaned** : cleaned skill label (lower case , no punctuation and remove description python (programming langauge) -> python )
- generate **skill_len** : length of skill_cleaned (number of tokens in skill_cleaned) : len(skill_cleaned.split(' '))
- generate **skill_stemmed** : stemmed skill_cleaned (see skillner/cleaner.py)
- generate **skill_lemmed**: lemmatized skill_cleaned (see skillner/cleaner.py)
- generate **match_on_stemmed** : True if skill_len == 1
- generate **abbreviation** : if found in db else ''

## 2. create token_dist.json 

this is step is simple we just ctockenize text to get the dist for each token in our skills db

```python
with open('./skillNer/data/skills_processed.json', 'r+') as f:
    skills_db = json.load(f)

def get_dist_new(array):
    words = []
    for val in array:
        vals = val.split(' ')
        for v in vals:

            words.append(v)

    a = words
    counter = collections.Counter(a)
    counter = dict(counter)
    return counter


n_grams = [skills_db[key]['skill_cleaned']
           for key in skills_db if skills_db[key]['skill_len'] > 1]
n_gram_dist = get_dist_new(n_grams)
# save
with open('./skillNer/data/token_dist.json', 'w', encoding='utf-8') as f:
    json.dump(n_gram_dist, f, ensure_ascii=False, indent=4)
```
## 3. create skill_db_relax_20.json

This script will generate the skill_db_relax_20.json i tried to document it so you can be able to modulate it for more redeability but what it do is some kind of data augmentation by generating surface forms for each skill . the augmentation is done given it len 
```python
# ============
# Script to generate skill db that support multiple surface forms for the matching procedure
# ============
import re
import collections
import json

with open('./skillNer/data/skills_processed.json', 'r+') as f:
    SKILL_DB = json.load(f)
with open('./skillNer/data/token_dist.json', 'r+') as f:
    dist = json.load(f)

RELAX_PARAM = 0.2
new_skill_db = {}
for key in SKILL_DB:
    high_surface_form = {}
    low_surface_form = []
    match_on_tokens = False
    skill_len = SKILL_DB[key]['skill_len']
    skill_name = SKILL_DB[key]['skill_name']
    skill_type = SKILL_DB[key]['skill_type']
    clean_name = SKILL_DB[key]['skill_cleaned']
    skill_lemmed = SKILL_DB[key]['skill_lemmed']
    skill_stemmed = SKILL_DB[key]['skill_stemmed']
    abv = SKILL_DB[key]['abbreviation']
    # param diferentiate software and gramatical skills
    uni_match_on_stemmed = SKILL_DB[key]['match_on_stemmed']

    # surface forms creation with some relaxation/enrichments 
    # to increase proba of matching with natural text

    if abv != '':

        high_surface_form['abv'] = abv
    # unigram skills
    if skill_len == 1:
        high_surface_form['full'] = clean_name
        if uni_match_on_stemmed:
            low_surface_form.append(skill_stemmed)
    # 2-gram skills (ex : project management )
    if skill_len == 2:
        high_surface_form['full'] = skill_lemmed
        # enricj with inverse skills project manag ->  manag project
        stemmed_tokens = skill_stemmed.split(' ')
        inv_stemmed_tokens = stemmed_tokens[::-1]
        low_surface_form.append(skill_stemmed)
        low_surface_form.append(' '.join(inv_stemmed_tokens))
        last = stemmed_tokens[-1]
        start = stemmed_tokens[0]
        # if last token of skill is unique let be identifier of the skill 
        # (works well with software where we may choose to use only one term )
        if dist[last] == 1:
            low_surface_form.append(last)
        # very noisy enrichment (to be deleted)
        """ 
        if dist[start]/dist[last] < RELAX_PARAM:
            low_surface_form.append(start)
        """

    if skill_len > 2:
        high_surface_form['full'] = skill_lemmed
        # if skill with more than 2 tokens the matcher can be on 
        # the skill tokens then we agg matches when scoring
        match_on_tokens = True
    # write skill
    new_skill_db[key] = {'skill_name': skill_name,
                         'skill_type': skill_type,
                         'skill_len': skill_len,
                         'high_surfce_forms': high_surface_form,
                         'low_surface_forms': low_surface_form,
                         'match_on_tokens': match_on_tokens
                         }

# add more surface forms to 2 gram skills (this code section might be deletd in the future )
list_ = []
for key in new_skill_db:
    low = new_skill_db[key]['low_surface_forms']
    skill_len = new_skill_db[key]['skill_len']
    if skill_len == 2:
        unique = [l for l in low if len(l.split(' ')) == 1]
        for a in unique:
            list_.append(a)


counter = collections.Counter(list_)

for key in new_skill_db:
    new_skill_db[key]['low_surface_forms']
    skill_len = new_skill_db[key]['skill_len']
    if skill_len == 2:
        low = new_skill_db[key]['low_surface_forms']
        new_l = []
        for l in low:
            if len(l.split(' ')) == 1:
                if counter[l] == 1:
                    new_l.append(l)
            else:
                new_l.append(l)
        new_skill_db[key]['low_surface_forms'] = new_l


# search for abreviation if found 'AQM (Advange quality mangement)' -> AQM 
# step 1 extract susptible abv using regex 
# step 2 check if abv is unique in the db (by looking at token dist )

n_grams = [SKILL_DB[key] for key in SKILL_DB if SKILL_DB[key]['skill_len'] > 1]
rx = r"\b[A-Z](?=([&.]?))(?:\1[A-Z])+\b"


def extract_sub_forms(skill_name):
    return [x.group() for x in re.finditer(rx, skill_name)]


def remove_btwn_par(str_):
    return re.sub("[\(\[].*?[\)\]]", "", str_)


subs = []
for n_skill in n_grams:
    skill_name = n_skill['skill_name']
    new_skill_name = remove_btwn_par(skill_name)
    sub_f = extract_sub_forms(new_skill_name)
    if sub_f != []:
        print(skill_name)
        print(sub_f)
        print('--------')
        for s in sub_f:
            subs.append(s)
dist = collections.Counter(subs)

for key in new_skill_db:
    if new_skill_db[key]['skill_len'] > 2:

        skill_name = new_skill_db[key]['skill_name']
        new_skill_name = remove_btwn_par(skill_name)
        skill_low = new_skill_db[key]['low_surface_forms']
        sub_abv = extract_sub_forms(new_skill_name)
        for abv in sub_abv:
            if dist[abv] == 1:
                skill_low.append(abv)
        new_skill_db[key]['low_surface_forms'] = skill_low

# final save file 
with open('./skillNer/data/skill_db_relax_20.json', 'w', encoding='utf-8') as f:
    json.dump(new_skill_db, f, ensure_ascii=False, indent=4)
```



