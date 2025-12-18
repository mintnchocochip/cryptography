import socket

import numpy as np
from sympy import Matrix


def eeuclid(a: int, b: int) -> tuple:
    r1 = a
    r2 = b
    ri = 1
    qi = 0
    x1, y1 = 1, 0
    x2, y2 = 0, 1
    xi, yi = 0, 0

    while ri > 0:
        qi = r1 // r2
        ri = r1 % r2
        if ri == 0:
            break
        xi = x1 - (x2 * qi)
        yi = y1 - (y2 * qi)
        x1, y1 = x2, y2
        x2, y2 = xi, yi

    return (x2, y2)


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


def decrypt(ciphertxt, key):
    K = np.array(matricize(key))

    det = int(np.round(np.linalg.det(K))) % 26
    if det == 0:
        return "Error: Key not invertible"

    inv = det
    for i in range(1, 26):
        if (det * i) % 26 == 1:
            inv = i
            break

    Ks = Matrix(K)
    Ks = Ks.adjugate()
    K_inv = np.array(Ks.tolist()) * inv % 26

    ciphertxt = list(ciphertxt.lower())
    C_nums = []
    for char in ciphertxt:
        C_nums.append(ord(char) - ord("a"))

    plaintxt = ""
    for i in range(0, len(C_nums), 3):
        C_row = np.array(C_nums[i : i + 3]).reshape(1, 3)
        P_row = (C_row @ K_inv) % 26
        for num in P_row.flatten():
            plaintxt += chr(int(num) + ord("a"))
    return plaintxt


def receive():
    s = socket.socket()
    ip, port = "127.0.0.1", 8080
    try:
        s.connect((ip, port))
        data = s.recv(1024).decode()
        data = data.split("||")
        key = data[0]
        ciphertxt = data[1]
        return (key, ciphertxt)
    finally:
        s.close()


if __name__ == "__main__":
    try:
        key, ciphertxt = receive()
        plaintxt = decrypt(ciphertxt, key)
        print(plaintxt)
    except Exception as e:
        print(f"Error: {e}")
