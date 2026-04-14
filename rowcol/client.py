import socket


def receive():
    s = socket.socket()
    port = 8080
    ip = "127.0.0.1"
    s.connect((ip, port))
    data = s.recv(1024).decode()
    s.close()
    return data


def decrypt(ciphertext, key):
    rows = len(ciphertext) // len(key)
    column_dict = {}
    pos = 0
    for k in sorted(key):
        column_dict[k] = ciphertext[pos : pos + rows]
        pos += rows

    matrix = [[""] * len(key) for _ in range(rows)]
    for k in key:
        col_index = k - 1
        column = column_dict[k]
        for row in range(rows):
            matrix[row][col_index] = column[row]

    plaintext = ""
    for row in matrix:
        plaintext += "".join(row)

    print(plaintext)
    return plaintext


if __name__ == "__main__":
    ciphertext = receive()
    key = eval(input("Enter the key to decrypt: "))
    plaintext = decrypt(ciphertext, key)
    print(f"{ciphertext} has been decrypted to - {plaintext.strip('*')}")
