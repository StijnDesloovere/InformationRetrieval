
import os


# Create a positional index that stores the positions of a word in each document that contains the word
def create_positional_index():
    positional_index = {}
    document = 1

    for filename in os.listdir('./Documents'):
        file = open('./Documents/' + filename, "r")
        position = 0

        for line in file:
            for word in line.split():
                # Remove special characters in sentences
                word = word.replace(',', '').replace('.', '').replace('"', '').lower()
                # Add a new word to the positional index
                if word not in positional_index:
                    positional_index[word] = {}
                # Add a new document entry to the word dictionary in the positional index
                if document not in positional_index[word]:
                    positional_index[word][document] = []

                positional_index[word][document].append(position)

                position += 1

        document += 1
    # print(positional_index)
    return positional_index

def reverse_index_keys(index):
    reversed_index = dict(map(lambda kv: (kv[0][::-1], kv[1]), index.items()))
    return reversed_index
