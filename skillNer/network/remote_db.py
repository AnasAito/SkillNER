import requests

# fetch / modify skills_db and tokens dist

dict_url_json = {
    "SKILL_DB": "https://raw.githubusercontent.com/AnasAito/Skillner-bucket/master/skillner/skill_db_relax_20.json?token=ANNTDEF4OOKUL5VRO4K22NLBEUMG6",
    "TOKEN_DIST": "https://raw.githubusercontent.com/AnasAito/Skillner-bucket/master/skillner/token_dist.json?token=ANNTDEG54DQVBXMHHPC3ZPTBEUMIM"
}


# json_name is "SKILL_DB" or "TOKEN_DIST"
def fetch_remote_json(
    json_name: str
) -> dict:

    url = dict_url_json[json_name]

    return requests.get(url).json()
