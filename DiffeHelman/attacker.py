import random
import socket
import time


def gen_private_key(q):
    return random.randint(2, q - 2)


def gen_public_key(alpha, private_key, q):
    return pow(alpha, private_key, q)


def connect_to_alice(retries=100, delay=0.1):
    ip = "127.0.0.1"
    port = 8090
    for _ in range(retries):
        try:
            s = socket.socket()
            s.connect((ip, port))
            payload = s.recv(4096).decode()
            return payload, s
        except ConnectionRefusedError:
            time.sleep(delay)
    raise ConnectionRefusedError(f"could not connect to {ip}:{port}")


def serve_bob(q, alpha, forged_public):
    ip = "127.0.0.1"
    port = 8091
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(5)
    c, addr = s.accept()
    try:
        c.send(f"{q}||{alpha}||{forged_public}".encode())
        bob_public = int(c.recv(4096).decode())
    finally:
        c.close()
        s.close()
    return bob_public


if __name__ == "__main__":
    payload, alice_sock = connect_to_alice()
    q_str, alpha_str, alice_public_str = payload.split("||")
    q = int(q_str)
    alpha = int(alpha_str)
    Ya = int(alice_public_str)

    Xd1 = gen_private_key(q)
    Yd1 = gen_public_key(alpha, Xd1, q)
    alice_sock.send(str(Yd1).encode())
    alice_sock.close()
    shared_with_alice = pow(Ya, Xd1, q)

    Xd2 = gen_private_key(q)
    Yd2 = gen_public_key(alpha, Xd2, q)
    Yb = serve_bob(q, alpha, Yd2)
    shared_with_bob = pow(Yb, Xd2, q)

    print("Attacker")
    print("User Input:")
    print(f"  prime number (q): {q}")
    print(f"  primitive root (alpha): {alpha}")
    print(f"Choose private key randomly -> (Xd1 = {Xd1}, Xd2 = {Xd2})")
    print(f"Compute public key -> (Yd1 = {Yd1}, Yd2 = {Yd2})")
    print(f"Public key from Alice -> {Ya}")
    print(f"Public key from Bob -> {Yb}")
    print(f"Common key between Alice and Attacker -> {shared_with_alice}")
    print(f"Common key between Bob and Attacker -> {shared_with_bob}")
