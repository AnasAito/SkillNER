import requests

# fetch / modify skills_db and tokens dist

dict_url_json = {
    "SKILL_DB": "https://raw.githubusercontent.com/AnasAito/Skillner-bucket/master/skillner/skill_db_relax_20.json",
    "TOKEN_DIST": "https://raw.githubusercontent.com/AnasAito/Skillner-bucket/master/skillner/token_dist.json"
}


# json_name is "SKILL_DB" or "TOKEN_DIST"
def fetch_remote_json(
    json_name: str
) -> dict:
    print('here')
    url = dict_url_json[json_name]
    print('here')
    resp = requests.get(url)
    print(resp)
    return resp.json()
