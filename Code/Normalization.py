# Aspect 3: Normalization
# b) Include the use of soundex to improve recall. Demonstrate the improvement.
import os
from Code.positional_index import create_positional_index, reverse_index_keys
from Code.boolean_query import *
import time
from timeit import Timer
import numpy as np
import matplotlib.pyplot as plt

#==============================================================================
# Soundex normalization
#==============================================================================
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

#==============================================================================
# Creat soundex positional index
#==============================================================================
def create_soundex_positional_index():
    positional_index = {}
    document = 1

    # Load the stop word list into memory
    with open('./Stopword-List.txt') as file:
        stopwords = list(word.rstrip() for word in file)

    for filename in os.listdir('./Documents'):
        file = open('./Documents/' + filename, "r")
        position = 0

        for line in file:
            for word in line.split():
                word = soundex(word)
                # Remove special characters in sentences
                word = word.replace(',', '').replace('.', '').replace('"', '').replace("'s", '')\
                    .replace('?', '').replace('(', '').replace(')', '')\
                    .lower()
                # Filter out stop words
                if word in stopwords:
                    position += 1
                    continue
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

soundex_index = create_soundex_positional_index()

#==============================================================================
# Getting soundex positional postinglist of terms
#==============================================================================
def get_sdx_posting_list(word) :
    word = soundex(word)
    if word in soundex_index:
        return soundex_index[word]
    else:
        return []

def sdx_docID(word):
    word = soundex(word)
    posting_list = get_sdx_posting_list(word)
    docid = posting_list.keys()
    return docid

def get_sdx_position(word,docid):
    word = soundex(word)
    return soundex_index[word][docid]
print(soundex('AND'))
print(soundex('OR'))
print(soundex('NOT'))

#==============================================================================
# Handling Soundex Query
#==============================================================================
def soundex_query_handler(query):
    query = query.split(" ")
    term = query[0]
    posting = get_sdx_posting_list(term)
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
                term = get_sdx_posting_list(term)
                documents = intersection(documents,term)
    
            elif(op == '||'):
                term = query[index]
                term = get_sdx_posting_list(term)
                documents = union(documents,term)
         
            elif(op == '!'):
                term = query[index]
                term = get_sdx_posting_list(term)
                documents = list(set(documents) - set(term))
    return documents

#==============================================================================
# Calculate execution time
#==============================================================================
def calculate_normal_time(queryList):
    execute_time = []
    for query in queryList:
        part_time = Timer("query_handler(query)","from __main__ import query_handler,query")
        execute_time.append(part_time.timeit(number=10000))
    # print(execute_time)
    return execute_time

def calculate_sdx_time(queryList):
    execute_time = []
    for query in queryList:
        part_time = Timer("soundex_query_handler(query)","from __main__ import soundex_query_handler,query")
        execute_time.append(part_time.timeit(number=10000))
    # print(execute_time)
    return execute_time

#==============================================================================
# Set testing cases
#==============================================================================
queryList = ['long AND cry','passed AND photons AND rip','poorer OR done NOT anonymous','highlighted OR strong AND muddy',
            'returned AND income OR touch NOT afford','markets OR january AND mirror NOT cord',
            'announcement AND browser OR creates OR improved NOT amplifer','wording OR rejection OR inventions NOT xbox NOT draft',
            'fixed AND crap OR boosted AND price OR mobiles NOT georgeta','fire AND firefox NOT fear OR lend AND iranian OR bloggers',
            'consumers AND responsible OR telephoning AND press OR question NOT press',
            'electrons OR atoms NOT wide OR range AND firefox OR gathered NOT websidestory',
            'exploited OR debut NOT codenamed AND won OR vary AND statistics NOT peak','collect AND rot OR templating NOT software OR handsets AND poorer NOT re-using',
            'damage AND added OR screening AND unlock OR movie AND quality AND bit NOT clearer',           
            'recall NOT failures OR regions AND console OR tip AND cord NOT seven OR almost AND rarity not incidents',
            'setting OR proof OR involves AND loopholes NOT lying OR recycled AND toxic NOT desire OR equivalent AND tonnes OR newer NOT waste',
            'brand AND acquisitons OR patched NOT nuisance AND division OR fewer AND experienced OR employee']

#==============================================================================
# Plot bar charts for execution time  
#==============================================================================
def plot_bar_result(queryList):
    x =list(range(len(queryList)))
    normal_time = calculate_normal_time(queryList)
    sdx_time = calculate_sdx_time(queryList)

    total_width, n = 0.8, 2
    width = total_width / n

    plt.figure(figsize=(10,5))
    plt.bar(x,normal_time,fc = '#446455',width = width, label = 'Normal Boolean query')
    for i in x:
        x[i] = x[i] + width
    plt.bar(x,sdx_time,fc = '#C7B19C',width = width,label = 'Soundex Boolean query')
    plt.title('The execution comparion between noraml query and soundex normal query')
    plt.xlabel('query')
    plt.ylabel('execution time')
    plt.legend()
    plt.show()
    return 
    
plot_bar_result(queryList)

