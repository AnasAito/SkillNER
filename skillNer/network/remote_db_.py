# native packs
from typing import Literal
import requests
import json
import base64


# general params
USERNAME = "AnasAito"
REPO_NAME = "SkillNER"
END_POINT = "https://api.github.com/repos"


class RemoteBucket:
    """Main class to fetch remote data base (db)
    """

    def __init__(
        self,
        token: str = "",
    ) -> None:
        """Constructor of the class

        Parameters
        ----------
        token : str, optional
            your GitHub token in case files are whithin a private repo, by default "" which is the case of a public repo
        """

        # params
        self.token = token

        # map name of db to its path in repo
        self.mapping_path_db = {
            "SKILL_DB": "buckets/skill_db_relax_20.json",
            "TOKEN_DIST": "buckets/token_dist.json"
        }
        return

    def fetch_db(
        self,
        db_name: Literal["SKILL_DB", "TOKEN_DIST"]
    ) -> dict:
        """[summary]

        Parameters
        ----------
        db_name : Literal[
            [description]
        """

        # params
        db_path = self.mapping_path_db[db_name]
        token = self.token

        return RemoteBucket.fetch_remote_db(db_name, token)

    @staticmethod
    def fetch_remote_db(
        path: str,  # path of file in repo
        token: str = "",  # generated github token
        # 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
    ) -> dict:
        """General function to fetch a content of a json file given its path

        Parameters
        ----------
        path : str
            path of the json file within the repo
        token: str, optional
            Your GitHub token in case of a private repo, by default "" which is the case of public repo

        Returns
        -------
        dict
            Returns a json file in a form of python dictionary
        """

        # compose url
        url = f"{END_POINT}/{USERNAME}/{REPO_NAME}/contents/{path}"

        # request details
        headers = {
            'Authorization': f'token {token}'
        }

        # send request and retreive content from resp
        # content is encoded in base64
        content = requests.get(
            url,
            headers=headers
        ).json()["content"]

        return RemoteBucket.decode_to_json(content)

    @staticmethod
    def decode_to_json(
        json_as_base64: str  # json encoded in a base64
    ) -> dict:
        """Function to decode a json to usual python dict object

        Parameters
        ----------
        json_as_base64 : str
            the json expressed in base 64

        Returns
        -------
        dict
            returns a json a python dict object
        """
        # decode base64
        binary_json = base64.b64decode(json_as_base64)

        # replace one quot with double quotes
        # preserve binary format
        binary_json = binary_json.decode().replace("'", '"').encode()

        # convert binary to dict
        return json.loads(binary_json)
