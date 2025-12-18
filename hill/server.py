import socket

import numpy as np


def matricize(key):
    ckey = []
    key = list(key)
    for i in range(len(key)):
        key[i] = ord(key[i]) - ord("a")

    while len(key) % 3 != 0:
        key.append(23)

    for i in range(0, len(key), 3):
        ckey.append(key[i : i + 3])
    return ckey


def encrypt(plaintxt, key):
    K = np.array(matricize(key))

    plaintxt = list(plaintxt.lower())
    while len(plaintxt) % 3 != 0:
        plaintxt.append("x")

    P_nums = []
    for char in plaintxt:
        P_nums.append(ord(char) - ord("a"))

    ciphertxt = ""
    for i in range(0, len(P_nums), 3):
        P_row = np.array(P_nums[i : i + 3]).reshape(1, 3)
        C_row = (P_row @ K) % 26
        for num in C_row.flatten():
            ciphertxt += chr(int(num) + ord("a"))
    return ciphertxt


def transmit(ciphertxt, key):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
    ip = "127.0.0.1"
    s.bind((ip, port))
    s.listen(5)
    print(f"Server listening on {ip}:{port}")

    while True:
        try:
            c, addr = s.accept()
            print(f"Connection from {addr}")
            try:
                c.sendall((key + "||" + ciphertxt).encode())
                print(f"Sent: {key}||{ciphertxt}")
            finally:
                c.close()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    s.close()


if __name__ == "__main__":
    plaintxt = "abcxyztuv"
    key = "gybnqkurp"
    encrypted = encrypt(plaintxt, key)
    print(f"Encrypted: {encrypted}")
    transmit(encrypted, key)
