import hashlib
import math
import random
import zlib

import numpy as np

P = 0.0001

PATH = 'text.txt'
RANDOM_STATE = random.randint(10, 100)


def get_unique_words_from_text(path: str):
    with open(path, encoding="utf8") as file:
        return set(file.read().split())


unique_words = get_unique_words_from_text(PATH)
NUMBER_OF_WORDS = len(unique_words)
print('words =  ', NUMBER_OF_WORDS)
# m = - ( n * ln(P) ) / ( ln2 ) ^ 2


CBF_SIZE = -math.ceil((NUMBER_OF_WORDS * np.log(P)) / (np.log(2) ** 2))
print('cbf size = ', CBF_SIZE)


def get_number_of_hash_functions(cbf_size, number_of_uw):
    return round((cbf_size / number_of_uw) * math.log(2))


COUNT_OF_HASH_FUNCS = get_number_of_hash_functions(CBF_SIZE, NUMBER_OF_WORDS)
print('hashes = ', COUNT_OF_HASH_FUNCS)


def random_salts(hashes_count: int):
    salts_t = [
        hashlib.sha224(bytes(np.random.RandomState(RANDOM_STATE).randint(
            0, 999_999))).hexdigest() for _ in range(hashes_count)
    ]
    return salts_t


salts = random_salts(CBF_SIZE)


def get_index_via_hash(obj: str, salt: str, cbf_length: int):
    return zlib.crc32(bytes(obj + salt, encoding='utf8')) % cbf_length


def countable_bloom_filter(objects: set, cbf_length: int, hashes_count: int):
    cbf_t = [0] * cbf_length
    salts_t = random_salts(hashes_count)
    for obj in objects:
        for i in range(hashes_count):
            index = get_index_via_hash(obj=obj, salt=salts_t[i], cbf_length=CBF_SIZE)
            cbf_t[index] += 1
    return cbf_t


def word_prob(word_t: str, cbf_size: int, salts_t: list, hashes_count: int):
    minimal_val = 1000000000 - 1

    for i in range(hashes_count):
        index = get_index_via_hash(obj=word_t, salt=salts_t[i], cbf_length=cbf_size)
        if cbf[index] < minimal_val:
            minimal_val = cbf[index]

    if minimal_val > 0:
        return 1 / minimal_val
    else:
        return 0


cbf = countable_bloom_filter(objects=unique_words, cbf_length=CBF_SIZE, hashes_count=COUNT_OF_HASH_FUNCS)
print('cbf',cbf)

words = ['sensor', 'they', 'spectrometers', 'conventional', 'flashlight', 'expert', 'experience']

for word in words:
    print(word_prob(word_t=word, cbf_size=CBF_SIZE, salts_t=salts, hashes_count=COUNT_OF_HASH_FUNCS))
