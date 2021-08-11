# process_n_gram ,process_uni_gram : filter and score 

# native packs
import collections
# installed packs
import numpy as np
# my packs
# 


class Utils:
    def __init__(self, nlp, skills_db):
        self.nlp = nlp
        self.skills_db = skills_db 

        self.sgram = [skills_db[key]['skill_stemmed'] for key in skills_db if skills_db[key]['skill_len']==2]
        self.sgrams_skills_tokens_dist =  self.get_dist(self.sgram)
        return

    def get_dist(self, array):
        words = []
        for val in array :
            vals = val.split(' ')
            for v in vals :

                words.append(v)

        a = words
        counter = collections.Counter(a)
        counter = dict(counter)
        # print(counter)
        max_ = max(list(counter.values()))
        min_ = min(list(counter.values()))

        if max_==min_ :
            ret = counter
        else :
            ret  = {k: 1-((v-min_)/(max_-min_)) for k, v in counter.items()}
        return ret

    def one_gram_sim(self, text_str, skill_str):
        # transform into sentence 
        text = text_str+' '+skill_str
        tokens = self.nlp(text)
        token1, token2 = tokens[0], tokens[1]
    # print(token1, token2)
        return token1.similarity(token2)

    def similarity(self, texts):
        doc1 = self.nlp(texts[0])
        doc2 = self.nlp(texts[1])
    
        return  doc1.similarity(doc2)

    def get_sim(self, skill_name, f, input_text):
        text = skill_name.lower().replace(f,'').strip()
        #print('props : ', skill_name,'/', f ,'/',input_text)
        #print('sim /',text,'/',input_text)
        return self.similarity([text,input_text])

    def make_one(self, cluster, len_):
        a = [1]*len_
        return [1*(i in cluster) for i,one in enumerate(a)]

    def split_at_values(self, lst, val):
        return [i for i, x in enumerate(lst) if x != val]
            
    def grouper(self, iterable,dist):
        prev = None
        group = []
        for item in iterable:
            if  prev==None or item - prev <= dist:
                group.append(item)
            else:
                yield group
                group = [item]
            prev = item
        if group:
            yield group
        
    def get_clusters (self, co_oc):
        clusters = []
        for i,row in enumerate(co_oc):
            clusts = list(self.grouper(self.split_at_values(row, 0),1))
            if clusts != [] :
                #print(i,[c for c in clusts if i in c][0])
                a = [c for c in clusts if i in c][0]
                if a not in clusters :
                    
                    clusters.append(a)
        return clusters

    def is_low_frequency(self, match_str,skill_id):
        skill_name = self.skills_db[skill_id]['skill_stemmed'].split(' ')
    
        if self.sgrams_skills_tokens_dist[skill_name[0]] >= self.sgrams_skills_tokens_dist[skill_name[1]]:
        
            return skill_name[0]==match_str
        else : 
            return skill_name[1]==match_str

    def retain(self, text, tokens, skill_id, sk_look, corpus) :
        ## get id 
        real_id = sk_look[skill_id].split('_1w')[0]
        ## get len 
        len_ = self.skills_db[real_id]['skill_len']
        len_condition = corpus[skill_id].dot(tokens)/len_
        
        s_gr = np.array(list(tokens))*np.array(list(corpus[skill_id]))
        def condition(x): return x == 1
        s_gr_ind = [idx for idx, element in enumerate(s_gr) if condition(element)][0]
        #print('len',len_,real_id,s_gr_ind )
        if len_condition >=0.5 : 
            #print('debug',debug[real_id] ,corpus[skill_id] ,tokens , len_condition  )
            if len_>2   :
                    #print('ngram', True , real_id)
                    score = len_condition
                    return (True , {'skill_id':real_id,
                                    'doc_node_id':  [i for i,val in enumerate(s_gr) if val==1],
                                    'score':round(score,2)
                                })
                
            if  self.is_low_frequency(text[s_gr_ind],real_id)   :
                    #print('2gram', look_up_ngram[real_id],"/", text[s_gr_ind] ,"/",' '.join(text))
                    score = self.get_sim(self.skills_db[real_id]['skill_lemmed'], text[s_gr_ind] ,' '.join(text))

                    return (True , {'skill_id':real_id,
                                    'score':round(score,2),
                                    'doc_node_id': [i for i,val in enumerate(s_gr) if val==1]
                                })
            return (False , '')

        else :
            return (False , '')
        
    def get_corpus(self, text, matches):
        len_ = len(text)
        corpus = []
        look_up = {}
        unique_skills = list(set([match['skill_id'] for match in matches]))
        skill_text_match_bin = [0]*len_
        for index,skill_id in enumerate(unique_skills) : 
            
            on_inds = [match['doc_node_id'] for match in matches if match['skill_id']==skill_id]
            skill_text_match_bin_updated = [(i in on_inds)*1 for i,_ in enumerate(skill_text_match_bin)]
            corpus.append(skill_text_match_bin_updated)
            look_up[index] = skill_id
                    
        return np.array(corpus) , look_up
        
    ## main functions
    def process_n_gram(self, matches,text_obj):
                    if len(matches)==0:
                        return matches
                    
                    # get text spans with  conflict 
                    text_tokens = text_obj.lemmed().split(' ')
                    len_ = len(text_tokens)
                    ## create corpus matrix  
                    corpus,look_up = self.get_corpus(text_tokens,matches)
                    ## generate spans 
                    co_occ = np.matmul(corpus.T, corpus) # co-occurence of tokens aij : co-occurence of token i with token j
                    clusters = self.get_clusters(co_occ)
                    ones = [ self.make_one(cluster,len_) for cluster in clusters]
                    spans = [(np.array(one),np.array([a_[0] for a_ in np.argwhere(corpus.dot(one)!=0)])) 
                            for one in ones]
                    # filter and score 
                    new_spans = []
                    for span in spans :
                        tokens,skill_ids = span 
                        new_skill_obj = []
                        for sk_id in skill_ids : 
                            retain_ , r_sk_id = self.retain(text_tokens , tokens,sk_id,look_up,corpus )
                            if   retain_ :
                                new_skill_obj.append(r_sk_id)
                        # get max for each span 
                        scores = [sk['score'] for sk in new_skill_obj]
                        if scores!=[]:
                            max_score_index = np.array(scores).argmax() 
                    
                            new_spans.append(new_skill_obj[max_score_index])                
                    
                    return new_spans
                
    def process_unigram(self, matches, text_obj):
                    original_text = text_obj.transformed_text.split(' ')                
                    res = []
                    for match in matches :
                        id_ = match['skill_id']
                        match_id = match['doc_node_id']

                        skill_str = self.skills_db[id_]['skill_cleaned']
                        #print(match_id)
                        text_str = original_text[match_id]
                        sim = self.one_gram_sim(skill_str,text_str)
                        #match['doc_node_id'] = [match['doc_node_id']] # for normalisation purpose

                            
                        res.append({'skill_id':id_,
                                    'doc_node_id':[match_id],
                                    'doc_node_value':match['doc_node_value'],
                                    'score':round(sim,2)})  
                    return res