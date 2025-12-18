import socket


def decrypt(str, key):
    plain = ""
    for char in str:
        if char.islower():
            plain += chr(((ord(char) - ord("a") - int(key)) % 26) + ord("a"))
        else:
            plain += chr(((ord(char) - ord("A") - int(key)) % 26) + ord("A"))
    return plain


def receive():
    s = socket.socket()
    port = 8080
    s.connect(("127.0.0.1", port))
    key = s.recv(1024).decode()
    txt = s.recv(1024).decode()
    s.close()
    return (key, txt)


if __name__ == "__main__":
    key, ciphertxt = receive()
    plaintxt = decrypt(ciphertxt, int(key))
    print("Received: ", ciphertxt)
    print("Decrypted: ", plaintxt)
