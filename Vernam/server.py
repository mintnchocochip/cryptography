import socket


def decrypt(cipher, key):
    if len(cipher) != len(key):
        return 0
    plain = ""
    for i in range(len(cipher)):
        if cipher[i].islower():
            temp = (ord(cipher[i]) - ord("a")) ^ (ord(key[i]) - ord("a"))
            plain += chr((temp % 26) + ord("a"))
        else:
            temp = (ord(cipher[i]) - ord("A")) ^ (ord(key[i]) - ord("A"))
            plain += chr((temp % 26) + ord("A"))
    return plain


def receive():
    s = socket.socket()
    port = 8080
    ip = "127.0.0.1"
    s.connect((ip, port))
    raw_data = b""
    while True:
        part = s.recv(1024)
        if not part:
            break
        raw_data += part
    s.close()
    full_data = raw_data.decode().split("\n")
    key = full_data[0].strip()
    cipher = full_data[1] if len(full_data) > 1 else ""
    return (key, cipher)


if __name__ == "__main__":
    key, cipher = receive()
    plain = decrypt(cipher, key)
    print("Received: ", cipher)
    print("Decrypted: ", plain)
