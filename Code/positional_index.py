import os


# Create a positional index that stores the positions of a word in each document that contains the word
def create_positional_index():
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


def reverse_index_keys(index):
    reversed_index = dict(map(lambda kv: (kv[0][::-1], kv[1]), index.items()))
    return reversed_index
