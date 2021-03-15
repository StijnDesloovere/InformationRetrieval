from Code.Btree import BTree, create_btree
from Code.positional_index import create_positional_index, reverse_index_keys
import re


def wildcard_query(query, btree, reversed_btree):
    result = []
    # Split query in strings divided by the wildcard
    characters = list(filter(None, re.split(r"(\*)", query)))

    print(characters)

    for idx, char in enumerate(characters):
        # Check for a star symbol before the string of characters
        if not idx == 0:
            if characters[idx-1] == "*":
                reversed_char = char[::-1]
                first_part = reversed_char[:-1]
                last_letter = reversed_char[-1]
                next_last_letter = chr(ord(last_letter)+1)
                result = reversed_btree.range(reversed_char, first_part+next_last_letter, [], [])
                print("found a star before " + str(char))
        # Check for a star symbol after the string of characters
        if not idx+1 == len(characters):
            if characters[idx+1] == "*":
                first_part = char[:-1]
                last_letter = char[-1]
                next_last_letter = chr(ord(last_letter)+1)
                result = btree.range(char, first_part+next_last_letter, [], [])
                print("found a star after " + str(char))

    print(result)


index = create_positional_index()
reversed_index = reverse_index_keys(index)
btree = create_btree(index)
reversed_btree = create_btree(reversed_index)
wildcard_query("*p", btree, reversed_btree)
