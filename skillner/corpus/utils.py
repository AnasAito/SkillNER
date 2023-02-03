import pickle
def unpickle_dict(blob_path):
    return pickle.load(blob_path)
LOADERS = {
        'loader_type' : lambda blob_path :unpickle_dict(loader_type)
    }