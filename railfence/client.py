import socket


def decrypt(cipher, depth):
    n = len(cipher)
    chars_per_rail = [n // depth] * depth
    remainder = n % depth
    for i in range(remainder):
        chars_per_rail[i] += 1
    plainlist = []
    start = 0
    for i in range(depth):
        end = start + chars_per_rail[i]
        plainlist.append(list(cipher[start:end]))
        start = end
    plaintext = []
    for i in range(n):
        rail = i % depth
        plaintext.append(plainlist[rail].pop(0))
    plaintext = "".join(plaintext)
    plaintext = plaintext.rstrip("*")
    print(plaintext)
    return plaintext


def receive():
    s = socket.socket()
    port = 8080
    ip = "127.0.0.1"
    s.connect((ip, port))
    data = s.recv(1024).decode()
    s.close()
    return data


if __name__ == "__main__":
    ciphertext = receive()
    depth = int(input("Enter the depth to decrypt: "))
    plaintext = decrypt(ciphertext, depth)
    print(f"{ciphertext} has been decrypted to - {plaintext}")
