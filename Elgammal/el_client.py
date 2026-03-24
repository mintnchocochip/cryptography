import random
import socket
import time
import sympy


def gen_private_key(q):
    return random.randint(2, q-2)

def gen_public_key(alpha, Xa, q):
    return pow(alpha, Xa, q)

def decrypt(C1, C2, Xa, q):
    K = pow(C1, Xa, q)
    K_inv = pow(K, -1, q)
    M = (C2 * K_inv) % q
    return M

def transmit_key(Ya):
    s = socket.socket()
    ip = "127.0.0.1"
    port = 8081
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(5)
    c, addr = s.accept()
    try:
        c.send(str(Ya).encode())
    finally:
        c.close()
    c2, addr2 = s.accept()
    try:
        data = c2.recv(4096).decode()
    finally:
        c2.close()
        s.close()
    return data

def receive(retries=100, delay=0.1):
    ip = "127.0.0.1"
    port = 8080
    for _ in range(retries):
        try:
            s = socket.socket()
            s.connect((ip, port))
            t = s.recv(4096).decode()
            s.close()
            return t
        except ConnectionRefusedError:
            time.sleep(delay)
    raise ConnectionRefusedError(f"could not connect to {ip}:{port}")

if __name__ == "__main__":
    kp = receive()
    kp = kp.split("||")
    q, alpha = int(kp[0]), int(kp[1])
    print("received q,alpha =", q, alpha)
    Xa = gen_private_key(q)
    Ya = gen_public_key(alpha, Xa, q)
    print("Xa,Ya =", Xa, Ya)
    cipher_text = transmit_key(Ya)
    C1, C2 = tuple([int(_) for _ in cipher_text.split("||")])
    print("received C1,C2 =", C1, C2)
    K_client = pow(C1, Xa, q)
    print("K_client =", K_client)
    plaintxt = decrypt(C1, C2, Xa, q)
    print("Original msg:", plaintxt)
