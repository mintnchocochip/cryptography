import socket


def genbigram(plaintxt):
    if len(plaintxt) % 2 != 0:
        plaintxt += "x"

    chars = list(plaintxt)
    bigram = []
    i = 0
    while i < len(chars):
        if i + 1 < len(chars):
            if chars[i] == chars[i + 1]:
                bigram.append([chars[i], "x"])
                i += 1
            else:
                bigram.append([chars[i], chars[i + 1]])
                i += 2
        else:
            bigram.append([chars[i], "x"])
            i += 1

    return bigram


def findrc(char, key):
    for i in range(5):
        for j in range(5):
            if key[i][j] == char:
                return (i, j)
    return (-1, -1)


def decrypt(ciphertxt, key):
    bigram = genbigram(ciphertxt)
    subbed = ""
    for sec in bigram:
        r1, c1 = findrc(sec[0], key)
        r2, c2 = findrc(sec[1], key)

        if r1 == r2:
            subbed += key[r1][(c1 - 1 + 5) % 5]
            subbed += key[r1][(c2 - 1 + 5) % 5]
        elif c1 == c2:
            subbed += key[(r1 - 1 + 5) % 5][c1]
            subbed += key[(r2 - 1 + 5) % 5][c2]
        else:
            subbed += key[r1][c2]
            subbed += key[r2][c1]
    return subbed


def receive():
    s = socket.socket()
    port = 8080
    s.connect(("127.0.0.1", port))
    data = s.recv(1024).decode()
    s.close()
    parts = data.split("||")
    key_data = parts[0]
    ciphertext = parts[1]
    key_rows = key_data.split("|")
    key = []
    for row_str in key_rows:
        key.append(row_str.split(","))
    return ciphertext, key


if __name__ == "__main__":
    ciphertxt, key = receive()
    plaintxt = decrypt(ciphertxt, key)
    print("Key Matrix:")
    for row in key:
        print(row)
    print(f"Received ciphertext: {ciphertxt}")
    print(f"Decrypted plaintext: {plaintxt}")
