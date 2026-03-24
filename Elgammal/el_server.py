import random
import socket
import time
import sympy


def generate_q_alpha():
    q = random.randint(pow(2,10), pow(2,15))
    while(not sympy.isprime(q)):
         q = random.randint(pow(2,10), pow(2,15))
    alpha = sympy.ntheory.primitive_root(q)
    return (q, alpha)

def encrypt(M, alpha, Ya, q):
    k = random.randint(2, q-2)
    C1 = pow(alpha, k, q)
    K = pow(Ya, k, q)
    C2 = (M * K) % q
    return (C1, C2), k

def transmit_key(q, alpha):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
    ip = "127.0.0.1"
    s.bind((ip, port))
    s.listen(5)
    c, addr = s.accept()
    try:
        c.send(f"{q}||{alpha}".encode())
    finally:
        c.close()
        s.close()

def receive_public_key(retries=100, delay=0.1):
    ip = "127.0.0.1"
    port = 8081
    for _ in range(retries):
        try:
            s = socket.socket()
            s.connect((ip, port))
            Ya = s.recv(4096).decode()
            s.close()
            return int(Ya)
        except ConnectionRefusedError:
            time.sleep(delay)
    raise ConnectionRefusedError(f"could not connect to {ip}:{port}")

def transmit_cipher(C1, C2, retries=100, delay=0.1):
    ip = "127.0.0.1"
    port = 8081
    for _ in range(retries):
        try:
            s = socket.socket()
            s.connect((ip, port))
            try:
                s.send(f"{C1}||{C2}".encode())
            finally:
                s.close()
            return
        except ConnectionRefusedError:
            time.sleep(delay)
    raise ConnectionRefusedError(f"could not connect to {ip}:{port}")

if __name__ == "__main__":
    q, alpha = generate_q_alpha()
    q = int(q)
    alpha = int(alpha)
    print("q,alpha =", q, alpha)
    transmit_key(q, alpha)
    Ya = int(receive_public_key())
    print("Ya =", Ya)
    M = int(input("Enter the message as an integer (< q): "))
    (C1, C2), k = encrypt(M, alpha, Ya, q)
    print("k =", k)
    print("C1, C2 =", C1, C2)
    transmit_cipher(C1, C2)
    print("Message encrypted & transmitted...")
