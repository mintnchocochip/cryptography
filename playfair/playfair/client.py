import socket


def genbigram(plaintxt):
    gen = len([plaintxt]) % 2
    if gen != 0:
        plaintxt += "x" * gen
    chars = list(plaintxt)
    bigram = []
    for i in range(0, len(chars) - 1, 2):
        if chars[i] == chars[i + 1]:
            bigram.append([chars[i], "x"])
        bigram.append([chars[i], chars[i + 1]])
    # print(bigram)
    return bigram


def findrc(str, key):
    for i in range(5):
        for j in range(5):
            if key[i][j] == str:
                return (i, j)
    return (
        -1,
        -1,
    )


def decrypt(plaintxt, key):
    bigram = genbigram(plaintxt)
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
    parts = data.split("|")
    key = list(map(int, parts[0].split(",")))
    ciphertext = list(map(int, parts[1].split(",")))
    return ciphertext, key


if __name__ == "__main__":
    ciphertxt, key = receive()
    plaintxt = decrypt(ciphertxt, key)
    print("Received: ", ciphertxt)
    print("Decrypted: ", plaintxt)
