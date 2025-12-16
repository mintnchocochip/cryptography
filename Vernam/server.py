import socket


def decrypt(ciphertext, key):
    if len(ciphertext) != len(key):
        return None
    plaintext = []
    for i in range(len(ciphertext)):
        plaintext.append(chr(ciphertext[i] ^ key[i]))
    return "".join(plaintext)


def receive_data():
    s = socket.socket()
    port = 8080
    s.connect(("127.0.0.1", port))
    data = s.recv(1024).decode()
    s.close()

    parts = data.split("|")
    key = list(map(int, parts[0].split(",")))
    ciphertext = list(map(int, parts[1].split(",")))

    return ciphertext, key


if __name__ == "__main__":
    ciphertext, key = receive_data()
    decrypted = decrypt(ciphertext, key)
    print("Decrypted: ", decrypted)
    print("Received: ", ciphertext)
