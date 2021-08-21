import requests

# fetch / modify skills_db and tokens dist

dict_url_json = {
    "SKILL_DB": "https://firebasestorage.googleapis.com/v0/b/test-firebase-aee35.appspot.com/o/skill_db_relax_20.json?alt=media&token=f58853d3-e7c0-4dad-9154-aa4fb3114f5b",
    "TOKEN_DIST": "https://firebasestorage.googleapis.com/v0/b/test-firebase-aee35.appspot.com/o/token_dist.json?alt=media&token=0d4a5022-7663-4135-9fe7-ce5cc665eec3"
}


# json_name is "SKILL_DB" or "TOKEN_DIST"
def fetch_remote_json(
    json_name: str
) -> dict:

    url = dict_url_json[json_name]

    return requests.get(url).json()
