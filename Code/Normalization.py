# Aspect 3: Normalization
# b) Include the use of soundex to improve recall. Demonstrate the improvement.
import os
from Code.boolean_query import union, intersection

# ==============================================================================
# Soundex normalization
# ==============================================================================


def soundex(query):
    #Step 1: lower the query lists, remove unalpha elements
    query = query.lower()
    letters = [char for char in query if char.isalpha()]
    lens = len(letters)
    #Step 2: save the first letter. Remove a,e,i,o,u,y,h,w.
    if lens < 1:
        return ""
    if lens == 1:
        return query + "000"

    to_remove = ('a','e','i','o','u','y','h','w')

    first_letter = letters[0]
    letters = letters[1:]
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"

    #Step 3: Replace all consonants (include the first letter) with digits
    to_replace = {('b','f','p','v'):1,('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}
    first_letter = [value if first_letter else first_letter 
                    for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]
    # Step 4: Replace all adjacent same digits with one digit.
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]

    # Step 5: If the saved letter’s digit is the same the resulting first digit, remove the digit (keep the letter)
    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])

    # Step 6: Append 3 zeros if result contains less than 3 digits.
    # Remove all except first letter and 3 digits after it.

    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    return string

# ==============================================================================
# Create soundex positional index
# ==============================================================================


def create_soundex_positional_index():
    positional_index = {}
    document = 1

    path = os.path.dirname(os.getcwd())
    stop_word_path = os.path.join(path, "Stopword-List.txt")
    document_path = os.path.join(path, "Documents")

    # Load the stop word list into memory
    with open(stop_word_path) as file:
        stopwords = list(word.rstrip() for word in file)

    for filename in os.listdir(document_path):
        file = open(os.path.join(document_path, filename), "r")
        position = 0

        for line in file:
            for word in line.split():
                # Remove special characters in sentences
                word = word.replace(',', '').replace('.', '').replace('"', '').replace("'s", '')\
                    .replace('?', '').replace('(', '').replace(')', '')\
                    .lower()
                # Filter out stop words
                if word in stopwords:
                    position += 1
                    continue
                word = soundex(word)
                # Add a new word to the positional index
                if word not in positional_index:
                    positional_index[word] = {}
                # Add a new document entry to the word dictionary in the positional index
                if document not in positional_index[word]:
                    positional_index[word][document] = []

                positional_index[word][document].append(position)

                position += 1

        document += 1

    return positional_index

# ==============================================================================
# Getting soundex positional postinglist of terms
# ==============================================================================


def get_sdx_posting_list(word, soundex_index) :
    word = soundex(word)
    if word in soundex_index:
        return soundex_index[word]
    else:
        return []


def sdx_docID(word, soundex_index):
    word = soundex(word)
    posting_list = get_sdx_posting_list(word, soundex_index)
    docid = posting_list.keys()
    return docid


def get_sdx_position(word, soundex_index, docid):
    word = soundex(word)
    return soundex_index[word][docid]

# ==============================================================================
# Handling Soundex Query
# ==============================================================================


def soundex_query_handler(query, soundex_index):
    query = query.split(" ")
    term = query[0]
    posting = get_sdx_posting_list(term, soundex_index)
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
                term = get_sdx_posting_list(term, soundex_index)
                documents = intersection(documents,term)
    
            elif op == '||':
                term = query[index]
                term = get_sdx_posting_list(term,soundex_index)
                documents = union(documents,term)
         
            elif op == '!':
                term = query[index]
                term = get_sdx_posting_list(term,soundex_index)
                documents = list(set(documents) - set(term))
    return documents


