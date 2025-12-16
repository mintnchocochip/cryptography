import socket


def generate_key(length):
    key = []
    seed = 12345
    for i in range(length):
        seed = (seed * 1103515245 + 12345) % (2**31)
        key.append(seed % 256)
    return key


def encrypt(plaintext, key):
    if len(plaintext) != len(key):
        return None
    ciphertext = []
    for i in range(len(plaintext)):
        ciphertext.append(ord(plaintext[i]) ^ key[i])
    return ciphertext


def send_data(ciphertext, key):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
    s.bind(("127.0.0.1", port))
    s.listen(5)
    c, addr = s.accept()
    try:
        key_str = ",".join(map(str, key))
        cipher_str = ",".join(map(str, ciphertext))
        data = key_str + "|" + cipher_str
        c.sendall(data.encode())
    finally:
        c.close()
        s.close()


if __name__ == "__main__":
    plaintext = "Secret Message"
    key = generate_key(len(plaintext))
    ciphertext = encrypt(plaintext, key)
    send_data(ciphertext, key)
    print("Data sent")
