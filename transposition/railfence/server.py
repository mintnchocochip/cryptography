import socket


def encrypt(plain, depth):
    if len(plain) % depth != 0:
        plain += "*" * (depth - (len(plain) % depth))
    cipherlist = [[] for _ in range(depth)]
    c = 0
    for i in plain:
        cipherlist[c % depth].append(i)
        c += 1
    cipher = ""
    for i in cipherlist:
        cipher += "".join(i)
    print(f"Encrypted {plain} as ==> {cipher}")
    return cipher


def transmit(ciphertext):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
    ip = "127.0.0.1"
    s.bind((ip, port))
    s.listen(5)
    c, addr = s.accept()
    try:
        c.sendall(ciphertext.encode())
    finally:
        c.close()
        s.close()


if __name__ == "__main__":
    plaintext = input("Enter the text to encrypt: ")
    depth = int(input("Enter the depth for the encryption:"))
    ciphertext = encrypt(plaintext, depth)
    print("Transmitting....\n")
    transmit(ciphertext)
