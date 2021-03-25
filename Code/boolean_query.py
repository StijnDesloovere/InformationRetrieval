# 2.a: Implement full boolean querying supporting AND, OR and NOT.
# from cyberbrain import trace
from Code.positional_index import create_positional_index, reverse_index_keys

p_index = create_positional_index()
r_index = reverse_index_keys(p_index)
# print(p_index)
# print(r_index)

#==============================================================================
# Getting positional postinglist of terms
#==============================================================================

def get_pos_posting_list(word) :
    if word in p_index:
        return p_index[word]
    else:
        return []

def docID(word):
    posting_list = get_pos_posting_list(word)
    docid = posting_list.keys()
    return docid

def get_position(word,docid):
    return p_index[word][docid]

#==============================================================================
# Posting List Intersection
#==============================================================================
def intersection(p1,p2):
    if p1 is not None and p2 is not None:
        intersection = list(set(p1) & set(p2))
        return intersection
    else:
        return []

#==============================================================================
# Posting List Union
#==============================================================================
def union(p1,p2):
    if p1 is not None and p2 is not None:
        union = list(set().union(p1,p2))
        return union
    else:
        return []

#==============================================================================
# Posting List Negation
#==============================================================================
def neg(p1,p2):
    if p1 is not None and p2 is not None:
        neg = list(set(p1) - set(p2))
        return neg
    else:
        return []

#==============================================================================
# Proximity intersection of postings lists
#==============================================================================
def prox_intersection(p1,p2):
    ans = []
    if p1 is not None and p2 is not None:                                                                  
        len1 = len(p1)
        len2 = len(p2)
        i = j = 0 
        while i != len1 and j != len2:
            if docID(p1[i]) == docID(p2[j]):
                        l = []
                        pp1 = get_position(p1[i])
                        pp2 = get_position(p2[j])                                           
    
                        plen1 = len(pp1)
                        plen2 = len(pp2)
                        ii = jj = 0 

#==============================================================================
# Handling Normal Query
#==============================================================================
def query_handler(query,inverted_index):
    query = query.split(" ")
    term = query[0]
    posting = get_pos_posting_list(term)
    documents = posting
    
    for index in range(1,len(query)):
        if(query[index] == "AND"):
            op = '&'
        elif(query[index]== "OR"):
            op = '||'
        elif(query[index]== "NOT"):
            op = '!'
        else:
            if(op == '&'):
                term = query[index]
                term = get_pos_posting_list(term)
                documents = intersection(documents,term)
    
            elif(op == '||'):
                term = query[index]
                term = get_pos_posting_list(term)
                documents = union(documents,term)
         
            elif(op == '!'):
                term = query[index]
                term = get_pos_posting_list(term)
                documents = list(set(documents) - set(term))
    return documents

#==============================================================================
# Testing case
#==============================================================================
get_pos_posting_list("market")
get_pos_posting_list("today")
get_pos_posting_list("tomorrow")
query1 = "market OR today"
query = "market OR today AND dafasfsd"
query_handler(query,p_index)
query_handler(query1,p_index)
