import math
import pickle

from os.path import exists
from nltk.corpus import words
from typing import List, Set
from collections import Counter, defaultdict

word_list = words.words()
wordle_words = [word for word in word_list if len(word) == 5]
delimeter = '-'


def order_word(chars: str) -> List[str]:
    if not chars:
        return wordle_words
    return [word for word in wordle_words if all(word[pos] == c for pos, c in enumerate(chars) if c != delimeter)]


def in_word_wrong_position(chars: str) -> List[str]:
    if not chars:
        return wordle_words
    return [word for word in wordle_words if all(word[pos] != c for pos, c in enumerate(chars) if c != delimeter)
            and all(c in word for c in chars if c != delimeter)]


def out_word(chars: str) -> List[str]:
    if not chars:
        return wordle_words
    return [word for word in wordle_words if not any(c in word for c in chars)]


def get_word(order_chars: str, in_chars_wrong_position1: str, in_chars_wrong_position2:str,  out_chars:str) -> Set[str]:
    return set(order_word(order_chars))\
        .intersection(set(in_word_wrong_position(in_chars_wrong_position1)))\
        .intersection(set(in_word_wrong_position(in_chars_wrong_position2)))\
        .intersection(set(out_word(out_chars)))


def bucketize(guess_word, actual_word):
    result = []
    for guess_c, actual_c in zip(guess_word, actual_word):
        if guess_c == actual_c:
            result.append(1)
        else:
            result.append(-1)
    guess_counter = Counter(guess_word)
    for i, c in enumerate(actual_word):
        if result[i] == -1 and guess_counter[c] > 0:
            result[i] = 0
            guess_counter[c] -= 1
    return ','.join([str(x) for x in result])


def default_dict_str():
    return defaultdict(str)


def get_or_serialize_all_buckets(words, file_name):
    if not exists(file_name):
        # bucket_map is not symmetric
        bucket_map = defaultdict(default_dict_str)
        for word1 in words:
            for word2 in words:
                bucket_map[word1][word2] = bucketize(word1, word2)
                bucket_map[word2][word1] = bucketize(word2, word1)
        file = open(file_name, "wb")
        pickle.dump(bucket_map, file)
        file.close()
    file = open(file_name, "rb")
    output = pickle.load(file)
    return output


def calculate_entropy(words, bucket_map, guess_word, debug=False):
    total_count = len(words)
    bucket_counter = Counter()
    for actual_word in words:
        bucket_counter[bucket_map[guess_word][actual_word]] += 1
    counts = bucket_counter.values()
    if debug:
        print(counts)
    entropy = 0
    for count in counts:
        prob = count * 1.0 / total_count
        entropy += prob * -1 * math.log2(1.0/count)
    return entropy


def sort_by_entropy(valid_words, all_words):
    return sorted(all_words, key=lambda word: calculate_entropy(valid_words, word))


if __name__ == '__main__':
    in_chars_wrong_position1 = ''
    in_chars_wrong_position2 = ''
    order_chars = ''
    out_chars = ''
    #words = get_word(order_chars, in_chars_wrong_position1, in_chars_wrong_position2, out_chars)
    #sorted_words = sort_by_entropy(wordle_words, wordle_words)
    #print(words)
    #print(sorted_words)
    #print(calculate_entropy(wordle_words, sorted_words[0], True))
    get_or_serialize_all_buckets(wordle_words, "./resource/buckets")
    print("done")