# 2.a: Implement full boolean querying supporting AND, OR and NOT.

# ==============================================================================
# Getting positional postinglist of terms
# ==============================================================================


def get_pos_posting_list(word, p_index):
    if word in p_index:
        return p_index[word]
    else:
        return []


def docID(word, p_index):
    posting_list = get_pos_posting_list(word, p_index)
    doc_id = posting_list.keys()
    return doc_id


def get_position(word, p_index, doc_id):
    return p_index[word][doc_id]

# ==============================================================================
# Posting List Intersection
# ==============================================================================


def intersection(p1, p2):
    if p1 is not None and p2 is not None:
        intersection = list(set(p1) & set(p2))
        return intersection
    else:
        return []


# ==============================================================================
# Posting List Union
# ==============================================================================


def union(p1, p2):
    if p1 is not None and p2 is not None:
        union = list(set().union(p1,p2))
        return union
    else:
        return []

# ==============================================================================
# Posting List Negation
# ==============================================================================


def neg(p1, p2):
    if p1 is not None and p2 is not None:
        neg = list(set(p1) - set(p2))
        return neg
    else:
        return []

# ==============================================================================
# Handling Normal Query
# ==============================================================================


def query_handler(query, p_index):
    query = query.split(" ")
    term = query[0]
    posting = get_pos_posting_list(term, p_index)
    documents = posting
    
    for index in range(1, len(query)):
        if query[index] == "AND":
            op = '&'
        elif query[index] == "OR":
            op = '||'
        elif query[index] == "NOT":
            op = '!'
        else:
            if op == '&':
                term = query[index]
                term = get_pos_posting_list(term, p_index)
                documents = intersection(documents, term)
    
            elif op == '||':
                term = query[index]
                term = get_pos_posting_list(term, p_index)
                documents = union(documents, term)
         
            elif op == '!':
                term = query[index]
                term = get_pos_posting_list(term)
                documents = list(set(documents) - set(term))
    return documents

