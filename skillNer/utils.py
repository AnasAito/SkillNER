# process_n_gram, process_uni_gram : filter and score

# native packs
import collections
import functools
import math

# installed packs
import numpy as np
# my packs
from skillNer.text_class import Text
from skillNer.general_params import  TOKEN_DIST

class Utils:
    def __init__(self, nlp, skills_db):
        self.nlp = nlp
        self.skills_db = skills_db
        self.token_dist = TOKEN_DIST
        self.sign = functools.partial(math.copysign, 1)
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
    
    def one_gram_sim(self, text_str, skill_str):
        # transform into sentence
        text = text_str + ' ' + skill_str
        tokens = self.nlp(text)
        token1, token2 = tokens[0], tokens[1]

        return token1.similarity(token2)
    def compute_w_ratio(self,simple_ratio ,skill_id,matched_tokens):
 


        up_max = max([self.token_dist[token] for token in matched_tokens ])

        scarsity = (1/up_max)
        return simple_ratio*(1+scarsity)
        
        
        
    
    def retain(self, text_obj , text, tokens, skill_id, sk_look, corpus):
        # get id
        #print(sk_look[skill_id])
        real_id,type_ = sk_look[skill_id].split('_')
        
        #print('----')
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
       

        if type_ == 'oneToken':
           # score = self.compute_w_ratio(len_condition/len_ , real_id,[text_obj[ind].lemmed  for ind in s_gr_n ])
            score = len_condition/len_
        if type_ == 'fullUni':
            score = 1
     
        if type_ == 'lowSurf':
            if len_ > 2 : 
                score =1
           
            else : 
               
                text_str = ' '.join([str(text_obj[i]) for i, val in enumerate(s_gr) if val == 1])
                skill_str = self.skills_db[real_id]['high_surfce_forms']['full']
                
                score = self.one_gram_sim(text_str,skill_str)
               # print('one_gram',text_str,skill_str,score)
            
        return  {'skill_id': real_id,
                               'doc_node_id':  [i for i, val in enumerate(s_gr) if val == 1],
                               'doc_node_value' : ' '.join([str(text_obj[i]) for i, val in enumerate(s_gr) if val == 1]) ,
                               'type': type_,
                               'score': score,
                               'len':len_condition
                               }
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
            span_scored_skills = []
            types = []
            scores = []
            lens = []
            for sk_id in skill_ids:
                #score skill 
                scored_sk_obj = self.retain(text_obj,text_tokens, tokens, sk_id, look_up, corpus)
                span_scored_skills.append(scored_sk_obj)
                types.append(scored_sk_obj['type'])
                lens.append(scored_sk_obj['len']) 
                scores.append(scored_sk_obj['score'])
            # extract best candiate for a given span 
            if 'oneToken' in types and len(set(types))>1 : 
                ## having a ngram skill with other types in span condiates :
                ## priotize skills with high match length if length >1
                id_ = np.array(scores).argmax()
                max_score = 0
                for i,len_ in enumerate(lens):
                    if len_>1 and types[i]=='oneToken'  :
                        if scores[i]>=max_score:
                            id_=i
                
                        
                new_spans.append(span_scored_skills[id_])
                               
                
            else :
                max_score_index = np.array(scores).argmax()
                new_spans.append(span_scored_skills[max_score_index])
                        

        return new_spans


