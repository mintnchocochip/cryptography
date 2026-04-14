import socket


def encrypt(plaintext, key):
    cols = len(key)
    pad = len(plaintext) % len(key)
    if pad != 0:
        pad = len(key) - pad
        plaintext += "*" * pad
    matrix = []
    for i in range(0, len(plaintext), cols):
        matrix.append(list(plaintext[i : i + cols]))
    print(matrix)
    column_list = {}
    for i in key:
        temp = ""
        for row in range(len(matrix)):
            temp += matrix[row][i - 1]
        column_list[i] = temp
    cipher = ""
    for k in sorted(key):
        cipher += column_list[k]
    print(f"Encrypted {plaintext} as ==> {cipher}")
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
    key = eval(input("Enter the key for the encryption:"))
    ciphertext = encrypt(plaintext, key)

    print("Transmitting....\n")
    transmit(ciphertext)
