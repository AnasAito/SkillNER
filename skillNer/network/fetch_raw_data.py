# native packs
import requests
import json
# installed packs
import pandas as pd
from pandas import json_normalize


auth_endpoint = "https://auth.emsicloud.com/connect/token"  # auth endpoint

# replace 'your_client_id' with your client id from your api invite email
client_id = "5f379hywuvh7fvan"
# replace 'your_client_secret' with your client secret from your api invite email
client_secret = "hfCkXQEy"
scope = "emsi_open"  # ok to leave as is, this is the scope we will used

# set credentials and scope
payload = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&scope={scope}"
# headers for the response
headers = {'content-type': 'application/x-www-form-urlencoded'}
access_token = json.loads((requests.request("POST", auth_endpoint, data=payload, headers=headers)).text)[
    'access_token']  # grabs request's text and loads as JSON, then pulls the access token from that


def fetch_skills_list() -> pd.DataFrame:

    # List of all skills endpoint
    all_skills_endpoint = "https://emsiservices.com/skills/versions/latest/skills"
    # Auth string including access token from above
    auth = f"Authorization: Bearer {access_token}"
    headers = {'authorization': auth}  # headers
    response = requests.request(
        "GET", all_skills_endpoint, headers=headers)  # response
    response = response.json()['data']  # the data

    # all_skills_df = pd.DataFrame(json_normalize(response)); # Where response is a JSON object drilled down to the level of 'data' key
    return response
