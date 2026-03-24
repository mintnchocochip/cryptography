import random
from sympy import isprime

def gen_prime(bits=16):
    while True:
        q = random.getrandbits(bits)
        if isprime(q):
            return q

def generate_alpha(q):
    return sympy.ntheory.primitive_root(q)

def gen_private_key(q):
    return random.randint(2, q-2)

def gen_public_key(alpha, Xa, q):
    return pow(alpha, Xa, q)

def encryption(M, alpha, Ya, q):
    k = random.randint(2, q-2)
    C1 = pow(alpha, k, q)
    K = pow(Ya, k, q)
    C2 = (M * K) % q
    return C1, C2

def decryption(C1, C2, Xa, q):
    K = pow(C1, Xa, q)
    K_inv = pow(K, -1, q)
    M = (C2 * K_inv) % q
    return M
