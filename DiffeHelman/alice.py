import random
import socket

import sympy


def generate_q_alpha():
    q = random.randint(pow(2, 10), pow(2, 15))
    while not sympy.isprime(q):
        q = random.randint(pow(2, 10), pow(2, 15))
    alpha = sympy.ntheory.primitive_root(q)
    return q, alpha


def gen_private_key(q):
    return random.randint(2, q - 2)


def gen_public_key(alpha, private_key, q):
    return pow(alpha, private_key, q)


def exchange_with_attacker(q, alpha, public_key):
    ip = "127.0.0.1"
    port = 8090
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(5)
    c, addr = s.accept()
    try:
        c.send(f"{q}||{alpha}||{public_key}".encode())
        attacker_public = int(c.recv(4096).decode())
    finally:
        c.close()
        s.close()
    return attacker_public


if __name__ == "__main__":
    q, alpha = generate_q_alpha()
    Xa = gen_private_key(q)
    Ya = gen_public_key(alpha, Xa, q)
    attacker_public = exchange_with_attacker(q, alpha, Ya)
    shared_key = pow(attacker_public, Xa, q)

    print("Alice")
    print("User Input:")
    print(f"  prime number (q): {q}")
    print(f"  primitive root (alpha): {alpha}")
    print(f"Choose private key randomly -> {Xa}")
    print(f"Compute public key -> {Ya}")
    print(f"Public key from attacker -> {attacker_public}")
    print(f"Common key between Alice and Attacker -> {shared_key}")
