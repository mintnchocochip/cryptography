import socket


def encrypt(str, key):
    ciphertxt = ""
    for char in str:
        if char.islower():
            ciphertxt += chr(((ord(char) - ord("a") + key) % 26) + ord("a"))
        else:
            ciphertxt += chr(((ord(char) - ord("A") + key) % 26) + ord("A"))
    return ciphertxt


def transmit(str, key):
    s = socket.socket()
    port = 8080
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        c.send(key.encode())
        c.send(str.encode())
        c.close()


if __name__ == "__main__":
    plaintxt = input("Enter the string to encrypt: ")
    key = int(input("Enter the shift value: "))

    transmit(encrypt(plaintxt, key), str(key))
