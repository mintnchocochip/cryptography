import socket


def Encrypt(plaintext, keyword):
    plaintext = plaintext.lower()
    keyword = keyword.lower()
    ciphertxt = ""
    for i in range(len(plaintext)):
        Ki = ord(plaintext[i]) - ord("a")
        Pi = ord(keyword[i]) - ord("a")
        ciphertxt += chr(((Ki ^ Pi) % 26) + ord("a"))
    print("Encoded text: " + ciphertxt)
    return ciphertxt


def transmit(string, key):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
    s.bind(("127.0.0.1", port))
    s.listen(5)
    print("Listening for connections...")
    while True:
        c, addr = s.accept()
        print(f"Connected to {addr}")
        try:
            c.sendall((key + "\n").encode())
            c.sendall((string + "\n").encode())
        finally:
            c.close()


if __name__ == "__main__":
    key = "abcde"
    cipher = Encrypt("hello", key)
    print("Sent: ", cipher, ", ", key)
    transmit(cipher, key)
