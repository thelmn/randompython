__author__ = 'NJORO'


def gcd(m, n):
    # using simple euclidean division
    n, m = abs(n), abs(m)
    if n > m:
        n, m = m, n
    while m % n != 0:
        m, n = n, m % n
    return n


def mod_inverse(a, m):
    # modular inverse is x solution to a*x = 1 (mod m)
    # using the extended euclid division method
    if gcd(a, m) != 1:
        return None  # mod inverse only exists if a,m are relatively prime
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3  # quotient through integer division operator //
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
