import random
import socket


def encryption(plain, Ya, a, q):
    k = random.randint(2, pow(2, 8))
    K = pow(Ya, k, q)
    C1 = pow(a, k, q)
    C2 = (K * plain) % q
    return (C1, C2)

def sharing(M):
    ip = "127.0.0.1"
    port = 8080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    try:
        public_key = client.recv(1024).decode()
        q, a, Ya = map(int, public_key.split(","))
        C1, C2 = encryption(M, Ya, a, q)
        client.send(f"{C1},{C2}".encode())
    finally:
        client.close()
    return (q, a, Ya, C1, C2)

if __name__ == "__main__":
    M = int(input("Enter integer message to encrypt: "))
    q, a, Ya, C1, C2 = sharing(M)
    print(f"Publ key: q={q}, a={a}, Ya={Ya}")
    print(f"Plaintext M={M}")
    print("Sent cipher pair:", (C1, C2))
