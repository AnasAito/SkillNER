# from typing import Callable
import os
import yaml
from .utils import LOADERS

CORPUS_ROOT = '/workspaces/SkillNER/skillner/corpus/knowledge_bases'

def read_yaml(path):
    with open(path, 'r') as stream:
        try:
            parsed_yaml=yaml.safe_load(stream)
            return  parsed_yaml
        except yaml.YAMLError as exc:
            print(exc)

def load_corpus(corpus_id:str,is_local:bool = True)->dict:
    """Load corpus by  ``corpus_id``.

    Parameters
    ----------
    corpus_id: String
        The id of knowledge base to be used by matcher.
    """
    
    if is_local : 
        # construct corpus path by corpu_id
        corpus_path = f"{CORPUS_ROOT}/{corpus_id.upper()}"
        # corpus_meta 
        corpus_meta = read_yaml(f"{corpus_path}/meta_data.yaml")
        # get loader_type
        loader_type = corpus_meta.get('loader_type')
        loader = LOADERS[loader_type]
        return {
            'corpus_blob' : loader(corpus_path),
            'corpus_meta' : corpus_meta}
    else : 
        pass

def load(corpus_id:str):
    """surface kb and query method  ``corpus_id``.

    Parameters
    ----------
    corpus_id: String
        The id of knowledge base to be used by matcher.
    """
    corpus  = load_corpus(corpus_id)
    knowledge_base = corpus['corpus_blob']
    def query_method(s: str):
        return knowledge_base.get(s, None)

    return knowledge_base,query_method

# test 
# print(load_corpus(corpus_id='esco_en',is_local= True))