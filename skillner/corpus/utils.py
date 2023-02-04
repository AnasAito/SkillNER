import pickle

def unpickle_dict(corpus_path):
    """
    :param corpus_path: Specify the path to the corpus folder
    :return: A dictionary of the form:
    """
    blob_path = f"{corpus_path}/blob.pkl"
    with open(blob_path, 'rb') as handle:
        data = pickle.load(handle)
    return data 


LOADERS = {
        'dict' : unpickle_dict}