# native packs
import requests


MAPPING_NAME_URL = {
    "SKILL_DB": "buckets/skill_db_relax_20.json",
    "TOKEN_DIST": "buckets/token_dist.json"
}


class RemoteBucket:
    """Main class to fetch data bases (db) from repo. db are saved in a `.json` files
    """

    def __init__(
        self,
        token: str = "",
        branch: str = "master"
    ) -> None:
        """Constructor of the class

        Parameters
        ----------
        token : str, optional
            Your GitHub token in case repo is private, by default "" which is the case of public repo
        branch : str, optional
            the branch from which to fetch db, by default "master"
        """

        # save params
        self.token = token
        self.branch = branch

        # construct endpoint
        self.end_point = f"https://raw.githubusercontent.com/AnasAito/SkillNER/{self.branch}"
        return

    def fetch_remote(
        self,
        db_name: str
    ) -> dict:
        """Function to fetch db

        Parameters
        ----------
        db_name : str in ["SKILL_DB", "TOKEN_DIST"]
            Name of the db to fetch

        Returns
        -------
        dict
            returns the db in format of a python dict object

        Examples
        --------
        >>> from skillNer.network.remote_db import RemoteBucket
        >>> buckets = RemoteBucket(
            branch="master"
        )
        >>> buckets.fetch_remote("SKILL_DB")
        ...
        """
        # request props
        url = f"{self.end_point}/{MAPPING_NAME_URL[db_name]}"

        # check if repo is private
        if self.token:
            headers = {
                'Authorization': f'token {self.token}'
            }
        else:
            headers = {}

        # fetch
        response = requests.get(
            url=url,
            headers=headers
        )

        # return content in json format
        return response.json()
