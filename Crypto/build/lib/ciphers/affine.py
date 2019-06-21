__author__ = 'NJORO'

import sys, random
from ciphers.consts import SYMBOLS
from my_math.gcd import gcd, mod_inverse


def get_key_parts(key):
    key_a = key // len(SYMBOLS)
    key_b = key % len(SYMBOLS)
    return key_a, key_b


def create_key(key_a, key_b, mod):
    return key_a * mod + key_b  # eg 23 = 2 * 10 + 3 (mod 10)


def get_random_key():
    while True:
        symbols_size = len(SYMBOLS)
        key_a = random.randint(2, symbols_size)
        key_b = random.randint(2, symbols_size)
        if gcd(key_a, symbols_size) == 1:
            return create_key(key_a, key_b, symbols_size)


def check_keys(key_a, key_b, mode):
    if key_a == 1 and mode == 'encrypt':
        return False, 'Affine cipher becomes very weak when key_a is 1'
    if key_b == 0 and mode == 'encrypt':
        return False, 'Affine cipher becomes very weak when key_b is 0'
    if key_a < 0 or key_b < 0 or key_b > len(SYMBOLS) - 1:
        return False, 'keys should be greater than 0 and key_b not greater than len(SYMBOLS'
    if gcd(key_a, len(SYMBOLS)) != 1:
        return False, 'key_a and len(SYMBOLS) should be relatively prime'
    return True, 'good keys'


def encrypt(key, message):
    key_a, key_b = get_key_parts(key)
    key_status, key_message = check_keys(key_a, key_b, 'encrypt')
    if key_status:
        cipher_text = ''
        symbols_size = len(SYMBOLS)
        for symbol in message:
            if symbol in SYMBOLS:
                symbol_index = SYMBOLS.find(symbol)
                # eg A index = 33. cipher = 33*key_a + key_b (mod 96)
                cipher_text += SYMBOLS[(symbol_index * key_a + key_b) % symbols_size]
            else:
                cipher_text += symbol  # append symbol as is
        return cipher_text
    return key_message  # key error


def decrypt(key, cipher):
    key_a, key_b = get_key_parts(key)
    key_status, key_message = check_keys(key_a, key_b, 'decrypt')
    if key_status:
        message_text = ''
        symbols_size = len(SYMBOLS)
        mod_inverse_key_a = mod_inverse(key_a, symbols_size)
        for symbol in cipher:
            if symbol in SYMBOLS:
                symbol_index = SYMBOLS.find(symbol)
                # in reverse order of encrypt. (index - key_b) * mod inverse of key_a (mod 96)
                message_text += SYMBOLS[((symbol_index - key_b) * mod_inverse_key_a) % symbols_size]
            else:
                message_text += symbol  # append as is
        return message_text
    return key_message  # key error


if __name__ == '__main__':
    message = """A computer would deserve to be called intelligent if it could deceive a human into believing that it was human." -Alan Turing"""
    key = get_random_key()
    print(key)
    cipher = encrypt(key, message)
    print(cipher)
    decipher = decrypt(key, cipher)
    print(decipher)
