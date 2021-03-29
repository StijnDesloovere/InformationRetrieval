from Code.positional_index import create_positional_index, reverse_index_keys
from Code.boolean_query import *
from Code.Normalization import create_soundex_positional_index, get_sdx_posting_list
from Code.btree import create_btree
from Code.wildcard_query import wildcard_query

# Create positional index and reverse positional index
positional_index = create_positional_index()
reverse_positional_index = reverse_index_keys(positional_index)

# Create soundex positional index
soundex_positional_index = create_soundex_positional_index()

# Create B-trees
binary_tree = create_btree(positional_index)
reversed_binary_tree = create_btree(reverse_positional_index)


# Return all documents that match the query
def query(user_query, use_soundex=False, p_index=positional_index, s_index=soundex_positional_index, btree=binary_tree, r_btree=reversed_binary_tree):
    query = user_query.split(" ")
    op = ''
    documents = []

    for index in range(0, len(query)):
        if query[index] == "AND":
            op = '&'
        elif query[index] == "OR":
            op = '||'
        elif query[index] == "NOT":
            op = '!'
        else:
            term = query[index]

            # Handle wildcard queries
            if "*" in term:
                terms = wildcard_query(term, p_index, btree, r_btree).values()
                term = {}
                for term_p_index in terms:
                    for k, v in term_p_index.items():
                        if k in term:
                            term[k] = sorted(term[k] + v)
                        else:
                            term[k] = v
            else:
                # Support a soundex
                if use_soundex:
                    term = get_sdx_posting_list(term, s_index)
                else:
                    term = get_pos_posting_list(term, p_index)

            if op == '&':
                documents = intersection(documents, term)

            elif op == '||':
                documents = union(documents, term)

            elif op == '!':
                documents = list(set(documents) - set(term))

            elif op == '':
                documents = list(set(term))
    return documents

def test_queries():
    query_1 = query("search AND engine AND google")
    print("Query 1: Documents " + str(query_1) + " contain the terms search, engine and google")
    query_2 = query("*c*mp*er")
    print("Query 2: Documents " + str(query_2) + " contain terms that match *c*mp*er (computer and supercomputer)")
    query_3 = query("*c*mp*er AND supercomputer")
    print("Query 3: Documents " + str(query_3) + " contain terms that match *c*mp*er and supercomputer")
    query_4 = query("*c*mp*er AND supercomputer", True)
    print("Query 4: Documents " + str(query_4) + " contain terms that match *c*mp*er and supercomputer with soundex")
    query_5 = query("*c*mp*er AND soepercomputer", True)
    print("Query 5: Documents " + str(query_5) + " contain terms that match *c*mp*er and soepercomputer with soundex")
    query_6 = query("move OR technology AND organisation")
    print("Query 6: Documents " + str(query_6) + " contain terms that match move or technology and organisation")
    query_7 = query("move OR technology AND organization")
    print("Query 7: Documents " + str(query_7) + " contain terms that match move or technology and organization")
    query_8 = query("move OR technology AND organisation", True)
    print("Query 8: Documents " + str(query_8) + " contain terms that match move or technology and organisation with soundex")
    query_9 = query("move OR technology AND organization", True)
    print("Query 9: Documents " + str(query_9) + " contain terms that match move or technology and organization with soundex")

test_queries()