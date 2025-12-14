import socket


def keygen(plaintext, partial_key):
    if not partial_key:
        return ""
    full_key = ""
    kp = 0
    for ch in plaintext:
        if ch.isalpha():
            k = partial_key[kp % len(partial_key)]
            if ch.islower():
                full_key += k.lower()
            else:
                full_key += k.upper()
            kp += 1
        else:
            full_key += ch
    return full_key


def encrypt(string, partial_key):
    full_key = keygen(string, partial_key)
    ciphertxt = ""
    for i, ch in enumerate(string):
        if not ch.isalpha():
            # preserve non-alphabet characters as-is
            ciphertxt += ch
            continue
        k = full_key[i]
        if ch.islower():
            ciphertxt += chr(((ord(ch) + ord(k) - 2 * ord("a")) % 26) + ord("a"))
        else:
            ciphertxt += chr(((ord(ch) + ord(k) - 2 * ord("A")) % 26) + ord("A"))
    return ciphertxt


def transmit(string, key):
    s = socket.socket()
    port = 8080
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        try:
            c.sendall((key + "\n").encode())
            c.sendall((string + "\n").encode())
        finally:
            c.close()


if __name__ == "__main__":
    plaintxt = input("Enter the plaintext to encrypt: ")
    key = input("Enter the key: ")
    full_key = keygen(plaintxt, key)
    ciph = encrypt(plaintxt, key)
    print(ciph)
    print(full_key)
    transmit(ciph, full_key)
    print("Sent")
