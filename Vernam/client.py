import socket


def encrypt(string, key):
    if len(string) != len(key):
        return 0
    cipher = ""
    for i in range(len(string)):
        if string[i].islower():
            temp = (ord(string[i]) - ord("a")) ^ (ord(key[i]) - ord("a"))
            cipher += chr((temp % 26) + ord("a"))
        else:
            temp = (ord(string[i]) - ord("A")) ^ (ord(key[i]) - ord("A"))
            cipher += chr((temp % 26) + ord("A"))
    return cipher


def transmit(string, key):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
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
    key = "Fiver"
    cipher = encrypt("Hello", "Fiver")
    transmit(cipher, "Fiver")
    print("Sent: " + cipher + ", " + key)
