import os
import pickle


DIR_KB = ".skillner-kb"


def download_kb():
    print(os.getcwd())
    print("called from terminal")

    with open(f"{DIR_KB}/ESCO_EN.pkl", "rb") as file:
        kb = pickle.load(file)
