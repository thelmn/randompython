__author__ = 'NJORO'

import random, os

from my_math.Primes import gen_large_prime
from my_math.gcd import gcd, mod_inverse

# in RSA converting message blocks to integer blocks prevents common attacks that work
#  on simple substitution ciphers eg dictionary attack, frequency analysis.
# characters in a block are converted to integers (eg by ascii encoding) then the integer array is combined
#  into one large block integer using place-value math (like 26 = 2*(10^1) + 6*(10^0) in decimal)

# a block size of 128 bits can represent values from 0 to (not including) 128^256
# eg in decimal, byte size is 10 (ie 0 to 9). for block size of 2 bytes(digits), values between
#  0 to (not including) 10^2 = 100 can be represented.
DEFAULT_BLOCK_SIZE = 128  # in BYTES. block size should be less than or equal to key size or RSA math fails
BYTE_SIZE = 256  # BITS. a byte can hold values 0 to 255


def get_blocks_from_text(message, block_size=DEFAULT_BLOCK_SIZE):
    # convert message into a list of block integers

    message_bytes = message.encode('ascii')  # returns a bytes object
    block_ints = []
    for block_start in range(0, len(message_bytes), block_size):
        block_int = 0  # int for this block
        for i in range(block_start, min(block_start + block_size, len(message))):  # min coz last block could be less
            # same as 26 = 2*(10^1) + 6*(10^0) with 10 being byte size and 0,1 being place-value(index)
            # i % block_size converts i into an index from 0 to block_size-1
            block_int += message_bytes[i] * (BYTE_SIZE ** (i % block_size))
        block_ints.append(block_int)
    return block_ints


def get_text_from_blocks(block_ints, message_length, block_size=DEFAULT_BLOCK_SIZE):
    # get back message text from a list of block integers.

    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(block_size-1, -1, -1):  # iterate backwards with step 1 to (not including) -1
            # i is now an index/place-value from 127 to 0
            # eg to decode 345: 3 = 345 // 10^2; 4 = 45 // 10^1; 5 = 5 //  10^0
            if len(message) + 1 < message_length:  # if the decoded message is still less than expected length
                place_value = BYTE_SIZE ** i
                ascii_number = block_int // place_value
                block_int %= place_value
                block_message.insert(0, chr(ascii_number))  # insert character at start of block message
        message.extend(block_message)  # add character list at end of message list
    return ''.join(message)


def encrypt_message(message, key, block_size=DEFAULT_BLOCK_SIZE):
    # (n, e) is the public key for encryption
    encrypted_blocks = []
    n, e = key

    for block in get_blocks_from_text(message, block_size):
        # cipher_text = message_text ^ e mod n
        # pow(a, b, c) is equivalent to (a ** b) % c
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks


def decrypt_message(encrypted_blocks, message_length, key, block_size=DEFAULT_BLOCK_SIZE):
    # (n, d) is the private key for decryption
    decrypted_blocks = []
    n, d = key

    for block in encrypted_blocks:
        # same as encrypt but with d instead of e
        decrypted_blocks.append(pow(block, d, n))
    # convert block ints into message text
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)


def read_key_file(key_filename):
    fo = open(key_filename)
    content = fo.read()
    fo.close()

    # key file content is <int key size>,<big int n>,<big int e or d>
    key_size, n, e_or_d = content.split(',')
    return int(key_size), int(n), int(e_or_d)


def generate_key(key_size):
    # gen p and q primes, and n
    p = gen_large_prime(key_size)
    q = gen_large_prime(key_size)
    n = p * q

    # get e that is relatively prime to (p -1)*(q -1)
    mod = (p - 1)*(q - 1)
    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if gcd(e, mod) == 1:
            break
    # get d modular inverse of e mod (p - 1)*(q - 1)
    d = mod_inverse(e, mod)

    public_key = n, e
    private_key = n, d
    # public, private keys can be swapped. ie any can encrypt but the other has to decrypt
    return public_key, private_key


def make_key_files(filename_prefix, key_size):
    private_key_filename = '%s_privkey.txt' % filename_prefix
    public_key_filename = '%s_pubkey.txt' % filename_prefix
    if os.path.exists(public_key_filename) or os.path.exists(private_key_filename):
        raise FileExistsError('Attempting to overwrite files %s. Use a different name' % filename_prefix)
    else:
        public_key, private_key = generate_key(key_size)
        fo = open(public_key_filename, 'w')
        fo.write('%s,%s,%s' % (key_size, public_key[0], public_key[1]))
        fo.close()
        fo = open(private_key_filename, 'w')
        fo.write('%s,%s,%s' % (key_size, private_key[0], private_key[1]))
        fo.close()
        return public_key, private_key


def encrypt_and_write_file(message, filename, block_size=DEFAULT_BLOCK_SIZE):
    key_size, n, e = read_key_file('%s_pubkey.txt' % filename)
    if key_size < block_size * 8:  # convert block size to BITS
        raise ArithmeticError('Block size should be equal to or less than key_size')
    else:
        public_key = n, e
        encrypted_blocks = encrypt_message(message, public_key, block_size)

        for i in range(len(encrypted_blocks)):
            encrypted_blocks[i] = str(encrypted_blocks[i])
        encrypted_content = ','.join(encrypted_blocks)

        encrypted_content = '%s_%s_%s' % (len(message), block_size, encrypted_content)

        fo = open('%s_cipher.txt' % filename, 'w')
        fo.write(encrypted_content)
        fo.close()

        return encrypted_content


def read_file_and_decrypt(filename):
    key_size, n, d = read_key_file('%s_privkey.txt' % filename)

    fo = open('%s_cipher.txt' % filename)
    content = fo.read()
    message_length, block_size, encrypted_content = content.split('_')
    message_length = int(message_length)
    block_size = int(block_size)

    if key_size < block_size * 8:  # convert block size to BITS
        raise ArithmeticError('Block size should be equal to or less than key_size')
    else:
        encrypted_blocks = []
        for block in encrypted_content.split(','):
            encrypted_blocks.append(int(block))

        return decrypt_message(encrypted_blocks, message_length, (n, d), block_size)


if __name__ == "__main__":
    message = '''"Journalists belong in the gutter because that is
where the ruling classes throw their guilty secrets." -Gerald Priestland
"The Founding Fathers gave the free press the protection it must have to bare the
secrets of government and inform the people." -Hugo Black'''
    filename = 'hugo'
    key_size = 1024
    make_key_files(filename, key_size)
    print(encrypt_and_write_file(message, filename))
    print(read_file_and_decrypt(filename))

