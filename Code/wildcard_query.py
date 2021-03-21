from Code.btree import BTree, create_btree
from Code.positional_index import create_positional_index, reverse_index_keys
import re


def wildcard_query(query, index, btree, reversed_btree):
    # Variables
    start_length = None
    end_length = None
    between = []
    intermediate_result = {}
    result = {}

    # Split query in strings divided by the wildcard
    characters = list(filter(None, re.split(r"(\*)", query)))

    # Help procedures
    def between_stars(i):
        if not i == 0 and not i + 1 == len(characters):
            return characters[i - 1] == "*" and characters[i + 1] == "*"

    def is_start(i):
        if not i + 1 == len(characters):
            return characters[i + 1] == "*"

    def is_end(i):
        if not i == 0:
            return characters[i - 1] == "*"

    # Process chars depending on if they fall between 2 star, have a star on the left or have a star on the right
    for idx, char in enumerate(characters):
        # Check if char should be in the middle of the word
        if between_stars(idx):
            between.append(char)
            continue
        # Check if char should be at the end of the word
        if is_end(idx):
            end_length = -len(char)
            reversed_char = char[::-1]
            first_part = reversed_char[:-1]
            last_letter = reversed_char[-1]
            next_last_letter = chr(ord(last_letter) + 1)
            reversed_words_in_range = reversed_btree.range(reversed_char, first_part + next_last_letter, [], {})
            words_in_range = reverse_index_keys(reversed_words_in_range)
            # If necessary perform an intersection
            if intermediate_result:
                intermediate_result = {x: intermediate_result[x] for x in intermediate_result if x in words_in_range}
            else:
                intermediate_result = words_in_range
        # Check if char should be in the beginning of the word
        if is_start(idx):
            start_length = len(char)
            first_part = char[:-1]
            last_letter = char[-1]
            next_last_letter = chr(ord(last_letter) + 1)
            intermediate_result = btree.range(char, first_part + next_last_letter, [], {})

    # Handle the case where the query starts and ends in a wildcard
    if not intermediate_result:
        intermediate_result = index

    # Check if the given character strings occur in the correct order
    if between:
        for k, v in intermediate_result.items():
            match_failed = False
            infix = k[start_length:end_length]  # infix = everything between the first chars and the last chars
            for char in between:
                char_pos = infix.find(char)
                if not char_pos == -1:
                    infix = infix[char_pos+len(char):]  # Look for the next chars in the remaining string
                else:
                    match_failed = True
                    continue

            if not match_failed:
                result[k] = v
    else:
        result = intermediate_result

    return result


# Example: find computer and supercomputer
index = create_positional_index()
reversed_index = reverse_index_keys(index)
btree = create_btree(index)
reversed_btree = create_btree(reversed_index)
print(wildcard_query("*c*mp*er", index, btree, reversed_btree))

