# ============
# Script to generate skill db that support multiple surface forms for the matching procedure

# the script use original emsi skill db can be downloaded using fetch.py
# download input db and place it in path
# ============
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

    # high_surface_form.append(clean_name)
    # high_surface_form.append(skill_lemmed)
    if abv != '':

        high_surface_form['abv'] = abv
    # unigram skills
    if skill_len == 1:
        high_surface_form['full'] = clean_name
        if uni_match_on_stemmed:
            low_surface_form.append(skill_stemmed)

    if skill_len == 2:
        high_surface_form['full'] = skill_lemmed

        stemmed_tokens = skill_stemmed.split(' ')
        inv_stemmed_tokens = stemmed_tokens[::-1]
        low_surface_form.append(skill_stemmed)
        low_surface_form.append(' '.join(inv_stemmed_tokens))
        last = stemmed_tokens[-1]
        start = stemmed_tokens[0]
        if dist[last] == 1:
            low_surface_form.append(last)
        if dist[start]/dist[last] < RELAX_PARAM:
            low_surface_form.append(start)

    if skill_len > 2:
        high_surface_form['full'] = skill_lemmed
        match_on_tokens = True
    # write skill
    new_skill_db[key] = {'skill_name': skill_name,
                         'skill_type': skill_type,
                         'skill_len': skill_len,
                         'high_surfce_forms': high_surface_form,
                         'low_surface_forms': low_surface_form,
                         'match_on_tokens': match_on_tokens
                         }

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

# save
with open('./skillNer/data/skill_db_relax_20.json', 'w', encoding='utf-8') as f:
    json.dump(new_skill_db, f, ensure_ascii=False, indent=4)
