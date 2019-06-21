__author__ = 'NJORO'
import random

from my_math.consts import PRIMES_10K


# Primality Testing with the Rabin-Miller Algorithm. Complex probabilistic test
def rabin_miller(num):
    # Return true if num is a prime
    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s //= 2
        t += 1

    for trials in range(5):  # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (v ** 2) % num
    return True


def is_prime(num):
    if num < 2:
        return False  # 0,1 not primes
    if num in PRIMES_10K:
        return True  # faster check than rabin_miller
    for prime in PRIMES_10K:
        if num % prime == 0:
            return False  # not prime if divisible by low primes
    # last resort is rabin_miller
    return rabin_miller(num)


def gen_large_prime(key_size = 1024):
    # Return a random prime number of key_size BITS in size.
    while True:
        num = random.randrange(2**(key_size - 1), 2**key_size)
        if is_prime(num):
            return num


def ihalf(x):
    return x // 2


def search(x, array):
    if x in [0, 1, 2]:
        return 2
    if len(array) == 1:
        return array[0]
    if len(array) == 2:
        return array[1]
    middle_index = ihalf(len(array) - 1)  # half of array length
    middle_item = array[middle_index]
    # print(middle_item)
    if x > middle_item:
        new_array = array[middle_index:]
        # print(new_array)
        return search(x, new_array)
    elif x < middle_item:
        new_array = array[:middle_index+1]
        # print(new_array)
        return search(x, new_array)
    else:
        return x


def nearest_high_prime(number):
    return search(number, PRIMES_10K)


if __name__ == "__main__":
    print(len(PRIMES_10K))
    print(nearest_high_prime(3))
    print(gen_large_prime())
