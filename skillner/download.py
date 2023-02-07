import os
import sys
import requests


DIR_KB = ".skillner-kb"
BASE_URL = (
    "https://github.com/AnasAito/SkillNER/raw/download-kb/.skillner-kb/{kb_name}.pkl"
)
SUPPORTED_KB = {"ESCO_EN"}


def download_kb():

    # get and validate name of KB
    if len(sys.argv) == 1:
        raise ValueError("Provide the name of Knowledge Base to download.")

    kb_name = sys.argv[1]
    kb_name = kb_name.upper()

    if kb_name not in SUPPORTED_KB:
        raise ValueError(
            f"Unsupported Knowledge Base. Excepted name of KB to in {SUPPORTED_KB} "
            f"but got {kb_name}"
        )

    # create dir KB
    dir_kb_exists = os.path.exists(DIR_KB)

    if not dir_kb_exists:
        os.makedirs(DIR_KB)

    # download KB
    print(f"Downloading {kb_name} ...")
    res = requests.get(BASE_URL.format(kb_name=kb_name))

    # save KB
    print(f"Saving {kb_name} ...")
    with open(f"{DIR_KB}/{kb_name}.pkl", "wb") as file:
        file.write(res.content)

    print(f"{kb_name} was downloaded successfully.")
