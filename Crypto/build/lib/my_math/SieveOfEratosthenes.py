__author__ = 'NJORO'

from math import sqrt

MAX_ARRAY_SIZE = 100


def isqrt(i):
    return int(sqrt(i))


def walk(array_size):
    a = [False] * 2 + [True] * (array_size - 1)  # 0, 1 not primes
    for i in range(2, isqrt(array_size) + 1):  # range(5, 10) => 5, 6, 7, 8, 9. add 1 to also eval 10
        if a[i]:
            for j in square_plus_multiples_gen(i, array_size):
                a[j] = False
    return [index for index, item in enumerate(a) if item]


def subsequent_multiples_walk():
    pass


def multiples_gen(prime, minimum, maximum):  # todo prevent re-fetching multiples from beginning for every block

    count = minimum // prime
    # print('start multiple %d' % count)
    while True:
        mult = prime * count
        if mult > maximum:
            break
        count += 1
        if mult >= minimum:
            yield mult


def square_plus_multiples_gen(i, maximum):
    count = 0
    while True:
        j = (i ** 2) + (i * count)
        if j > maximum:
            break
        else:
            count += 1
            yield j


def generate_primes(upper_limit):
    if upper_limit < 1:
        return []
    if upper_limit > MAX_ARRAY_SIZE:
        block_size = isqrt(upper_limit)
        print(block_size)
        a = walk(block_size)
        # print(a)
        for index in range(block_size + 1, upper_limit, block_size):
            if upper_limit - index < block_size:
                block_size = upper_limit - index
            b = [True] * block_size
            # print('index - %d' % index)
            # print([_index + index for _index, item in enumerate(b)])
            for i, prime in enumerate(a):
                # print('prime - {}'.format(prime))
                block_upper_limit = index + block_size - 1
                for multiple in multiples_gen(prime, index, block_upper_limit):
                    # print('multiple - %d' % multiple)
                    b[multiple - index] = False
                    # print(multiple - index)
            b = [_index + index for _index, item in enumerate(b) if item]
            # print(b)
            a += b
        return a
    else:
        return walk(upper_limit)


if __name__ == "__main__":
    a = generate_primes(100000)
    print(a)
    a = generate_primes(98)
    print(a)
