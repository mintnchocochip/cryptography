import random
import socket

import sympy


def keygeneration():
    q = 4
    while not sympy.isprime(q):
        q = random.randint(pow(2, 10), pow(2, 14))
    a = sympy.ntheory.primitive_root(q)
    Xa = random.randint(2, q - 2)
    Ya = pow(a, Xa, q)
    return (q, a, Xa, Ya)

def decryption(C1, C2, Xa, a, q):
    K = pow(C1, Xa, q)
    M = (C2 * pow(K, -1, q)) % q
    return M

def communication(q,a,Ya):
    ip = "127.0.0.1"
    port = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    try:
        c, addr = server.accept()
        public_key = f"{q},{a},{Ya}"
        c.send(public_key.encode())
        cipher_text = c.recv(1024).decode()
        C1, C2 = map(int, cipher_text.split(","))
    finally:
        pass
    return (C1, C2)

if __name__ == "__main__":
    q, a, Xa, Ya = keygeneration()
    C1,C2 = communication(q,a,Ya)
    print(f"Publ key: q={q}, a={a}, Ya={Ya}")
    print(f"Pvt key Xa={Xa}")
    M = decryption(C1, C2, Xa, a, q)
    print("Received cipher pair:", (C1, C2))
    print("Decrypted message:", M)
