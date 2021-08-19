# process_n_gram, process_uni_gram : filter and score

# native packs
import collections
# installed packs
import numpy as np
# my packs
from skillNer.text_class import Text
from skillNer.general_params import  S_GRAM_TOOLS_LINKS

class Utils:
    def __init__(self, nlp, skills_db):
        self.nlp = nlp
        self.skills_db = skills_db

        self.sgram = [skills_db[key]['skill_stemmed']
                      for key in skills_db if skills_db[key]['skill_len'] ==2]
        self.ngram = [skills_db[key]['skill_stemmed']
                      for key in skills_db if skills_db[key]['skill_len'] >1]
        self.sgrams_skills_tokens_dist = self.get_dist(self.sgram)
        self.ngrams_skills_tokens_dist = self.get_dist_new(self.ngram)
        
        return

    def get_dist(self, array):
        words = []
        for val in array:
            vals = val.split(' ')
            for v in vals:

                words.append(v)

        a = words
        counter = collections.Counter(a)
        counter = dict(counter)
        # print(counter)
        max_ = max(list(counter.values()))
        min_ = min(list(counter.values()))

        if max_ == min_:
            ret = counter
        else:
            ret = {k: 1-((v-min_)/(max_-min_)) for k, v in counter.items()}
        return ret
    
    def get_dist_new(self, array):
        words = []
        for val in array:
            vals = val.split(' ')
            for v in vals:

                words.append(v)

        a = words
        counter = collections.Counter(a)
        counter = dict(counter)
        return counter
    
    def one_gram_sim(self, text_str, skill_str):
        # transform into sentence
        text = text_str + ' ' + skill_str
        tokens = self.nlp(text)
        token1, token2 = tokens[0], tokens[1]

        return token1.similarity(token2)

    def similarity(self, texts):
        doc1 = self.nlp(texts[0])
        doc2 = self.nlp(texts[1])

        return doc1.similarity(doc2)

    def get_s_gram_score(self,skill_id, skill_name, f, input_text,is_tool,full_matches_ids):
        if is_tool : 
            inter =  list(set(S_GRAM_TOOLS_LINKS[skill_id])&set(full_matches_ids))
            #print(skill_id,S_GRAM_TOOLS_LINKS[skill_id],full_matches_ids)
            return len(inter)
        else :
            text = skill_name.lower().replace(f, '').strip()
            return self.similarity([text, input_text])

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

    def is_low_frequency(self, match_str, skill_id):
        skill_name = self.skills_db[skill_id]['skill_stemmed'].split(' ')

        if self.sgrams_skills_tokens_dist[skill_name[0]] >= self.sgrams_skills_tokens_dist[skill_name[1]]:

            return skill_name[0] == match_str
        else:
            return skill_name[1] == match_str
    def compute_w_ratio(self,skill_id,matched_tokens):
        
        skill_name = self.skills_db[skill_id]['skill_stemmed'].split(' ')
       # print(skill_name, [self.ngrams_skills_tokens_dist[token] for token in skill_name ])
        up = sum([1/self.ngrams_skills_tokens_dist[token] for token in matched_tokens ])
        
        down = sum([1/self.ngrams_skills_tokens_dist[token] for token in skill_name ])
        return up/down
        
    def retain(self, text_obj , text, tokens, skill_id, sk_look, corpus,full_matches_ids):
        # get id
        real_id = sk_look[skill_id].split('_1w')[0]
        # get len
        len_ = self.skills_db[real_id]['skill_len']
        ## get tokens ratio (over skill tokens lingth)  that matched with skill within span tokens !
        len_condition = corpus[skill_id].dot(tokens)/len_ 

        s_gr = np.array(list(tokens))*np.array(list(corpus[skill_id]))
        def condition(x): return x == 1
        s_gr_ind = [idx for idx, element in enumerate(
            s_gr) if condition(element)][0]
        s_gr_n = [idx for idx, element in enumerate(
            s_gr) if condition(element)]
        weighted_ratio = self.compute_w_ratio(real_id,[text_obj[ind].stemmed  for ind in s_gr_n ])


        return (True, {'skill_id': real_id,
                               'doc_node_id':  [i for i, val in enumerate(s_gr) if val == 1],
                               'doc_node_value' : ' '.join([str(text_obj[i]) for i, val in enumerate(s_gr) if val == 1]) ,
                               'score': round(weighted_ratio, 2)
                               })



    def get_corpus(self, text, matches):
        len_ = len(text)
        corpus = []
        look_up = {}
        unique_skills = list(set([match['skill_id'] for match in matches]))
        skill_text_match_bin = [0]*len_
        for index, skill_id in enumerate(unique_skills):

            on_inds = [match['doc_node_id']
                       for match in matches if match['skill_id'] == skill_id]
            skill_text_match_bin_updated = [
                (i in on_inds)*1 for i, _ in enumerate(skill_text_match_bin)]
            corpus.append(skill_text_match_bin_updated)
            look_up[index] = skill_id

        return np.array(corpus), look_up

    # main functions
    def process_n_gram(self, matches, text_obj: Text , full_matches_ids):
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
                    text_tokens, tokens, sk_id, look_up, corpus,full_matches_ids)
                if retain_:
                    new_skill_obj.append(r_sk_id)
            # get max scoring candidate for each span
            scores = [sk['score'] for sk in new_skill_obj]
            if scores != []:
                max_score_index = np.array(scores).argmax()

                new_spans.append(new_skill_obj[max_score_index])

        return new_spans

    def process_unigram(self, matches, text_obj: Text):
        original_text = text_obj.transformed_text.split(' ')
        res = {}
        for match in matches:
            id_ = match['skill_id']
            match_id = match['doc_node_id']

            skill_str = self.skills_db[id_]['skill_cleaned']
            # print(match_id)
            text_str = original_text[match_id]
            sim = self.one_gram_sim(skill_str, text_str)
            # match['doc_node_id'] = [match['doc_node_id']] # for normalisation purpose
            if match_id in res.keys():
                if sim >= res[match_id]['score']:
                    res[match_id] = {'skill_id': id_,
                                     'doc_node_id': [match_id],
                                     'doc_node_value': match['doc_node_value'],
                                     'score': round(sim, 2)}
                else:
                    pass
            else:

                res[match_id] = {'skill_id': id_,
                                 'doc_node_id': [match_id],
                                 'doc_node_value': match['doc_node_value'],
                                 'score': round(sim, 2)}

        return list(res.values())
