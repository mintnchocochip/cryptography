import random
import socket
import time


def gen_private_key(q):
    return random.randint(2, q - 2)


def gen_public_key(alpha, private_key, q):
    return pow(alpha, private_key, q)


def receive_from_attacker(retries=100, delay=0.1):
    ip = "127.0.0.1"
    port = 8091
    for _ in range(retries):
        try:
            s = socket.socket()
            s.connect((ip, port))
            payload = s.recv(4096).decode()
            return payload, s
        except ConnectionRefusedError:
            time.sleep(delay)
    raise ConnectionRefusedError(f"could not connect to {ip}:{port}")


if __name__ == "__main__":
    payload, sock = receive_from_attacker()
    q_str, alpha_str, forged_public_str = payload.split("||")
    q = int(q_str)
    alpha = int(alpha_str)
    forged_public = int(forged_public_str)

    Xb = gen_private_key(q)
    Yb = gen_public_key(alpha, Xb, q)
    sock.send(str(Yb).encode())
    sock.close()

    shared_key = pow(forged_public, Xb, q)

    print("Bob")
    print("User Input:")
    print(f"  prime number (q): {q}")
    print(f"  primitive root (alpha): {alpha}")
    print(f"Choose private key randomly -> {Xb}")
    print(f"Compute public key -> {Yb}")
    print(f"Public key from attacker -> {forged_public}")
    print(f"Common key between Bob and Attacker -> {shared_key}")
