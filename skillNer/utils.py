# process_n_gram, process_uni_gram : filter and score

# native packs
import collections
import functools
import math

# installed packs
import numpy as np
# my packs
from skillNer.text_class import Text
from skillNer.general_params import  S_GRAM_TOOLS_LINKS

class Utils:
    def __init__(self, nlp, skills_db):
        self.nlp = nlp
        self.skills_db = skills_db


        return


    

    




    def make_one(self, cluster, len_):
        a = [1] * len_
        return [1*(i in cluster) for i, one in enumerate(a)]

    def split_at_values(self, lst, val):
        return [i for i, x in enumerate(lst) if x != val]

    def grouper(self, iterable, dist):
        prev = None
        group = []
        for item in iterable:
            if prev == None or item - prev <= dist:
                group.append(item)
            else:
                yield group
                group = [item]
            prev = item
        if group:
            yield group

    def get_clusters(self, co_oc):
        clusters = []
        for i, row in enumerate(co_oc):
            clusts = list(self.grouper(self.split_at_values(row, 0), 1))
            if clusts != []:
                #print(i,[c for c in clusts if i in c][0])
                a = [c for c in clusts if i in c][0]
                if a not in clusters:

                    clusters.append(a)
        return clusters



        
    def retain(self, text_obj , text, tokens, skill_id, sk_look, corpus):
        # get id
        real_id = sk_look[skill_id].split('_1w')[0]
        # get len
        len_ = self.skills_db[real_id]['skill_len']
        ## get tokens ratio (over skill tokens lingth)  that matched with skill within span tokens !
        len_condition = corpus[skill_id].dot(tokens)

        s_gr = np.array(list(tokens))*np.array(list(corpus[skill_id]))
        def condition(x): return x == 1
        s_gr_ind = [idx for idx, element in enumerate(
            s_gr) if condition(element)][0]
        s_gr_n = [idx for idx, element in enumerate(
            s_gr) if condition(element)]
       


        return (True, {'skill_id': real_id,
                               'doc_node_id':  [i for i, val in enumerate(s_gr) if val == 1],
                               'doc_node_value' : ' '.join([str(text_obj[i]) for i, val in enumerate(s_gr) if val == 1]) ,
                               'len': len_condition,
                               'score': len_condition / len_
                               })



    def get_corpus(self, text, matches):
        len_ = len(text)
        corpus = []
        look_up = {}
        unique_skills = list(set([match['skill_id'] for match in matches]))
        skill_text_match_bin = [0]*len_
        for index, skill_id in enumerate(unique_skills):

            on_inds_ = [match['doc_node_id']
                       for match in matches if match['skill_id'] == skill_id]
            on_inds = [j for sub in on_inds_ for j in sub]
            skill_text_match_bin_updated = [
                (i in on_inds)*1 for i, _ in enumerate(skill_text_match_bin)]
            corpus.append(skill_text_match_bin_updated)
            look_up[index] = skill_id

        return np.array(corpus), look_up

    # main functions
    def process_n_gram(self, matches, text_obj: Text ):
        if len(matches) == 0:
            return matches

        # get text spans with  conflict
        text_tokens = text_obj.lemmed(as_list=True)
        len_ = len(text_tokens)
        # create corpus matrix
        corpus, look_up = self.get_corpus(text_tokens, matches)
        # generate spans
        # co-occurence of tokens aij : co-occurence of token i with token j
        co_occ = np.matmul(corpus.T, corpus)
        clusters = self.get_clusters(co_occ)
        ones = [self.make_one(cluster, len_) for cluster in clusters]
        spans = [(np.array(one), np.array([a_[0] for a_ in np.argwhere(corpus.dot(one) != 0)]))
                 for one in ones]
        # filter and score
        new_spans = []
        for span in spans:
            tokens, skill_ids = span
            new_skill_obj = []
            for sk_id in skill_ids:
                retain_, r_sk_id = self.retain(text_obj,
                    text_tokens, tokens, sk_id, look_up, corpus)
                if retain_:
                    new_skill_obj.append(r_sk_id)
            # get max scoring candidate for each span
            scores = [sk['len'] for sk in new_skill_obj]
            
            if scores != []:
                max_score = max(scores)
                
                max_score_indexs =[i for i,sk in enumerate(scores) if sk==max_score]
                if len(max_score_indexs)>1 :
                    for max_id in max_score_indexs : 
                        skill_id = new_skill_obj[max_id]['skill_id']
                        ## for 1,2 priority to uni and 2_gram
                        if max_score in [1,2] :
                            
                            if self.skills_db[skill_id]['skill_len']==2 or self.skills_db[skill_id]['skill_len']==1 :
                                new_skill_obj[max_id]['score']=1
                                new_spans.append(new_skill_obj[max_id])
                
                else : 
                    max_ind = max_score_indexs[0]
                    
                    new_spans.append(new_skill_obj[max_ind])
                        

        return new_spans


