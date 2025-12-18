import socket


def remcommon(st):
    visited = []
    for i in st:
        if i not in visited:
            visited.append(i)
    return "".join(visited)


def keygen(key):
    temp = ""
    if "i" in key:
        temp = "j"
    elif "j" in key:
        temp = "i"
    else:
        temp = "i"
    keychar = remcommon(key.lower())
    matval = remcommon(keychar.lower() + "abcdefgh" + temp + "klmnopqrstuvwxyz")

    key_matrix = []
    idx = 0
    for i in range(5):
        row = []
        for j in range(5):
            row.append(matval[idx])
            idx += 1
        key_matrix.append(row)
    return key_matrix


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


def encrypt(plaintxt, key):
    bigram = genbigram(plaintxt)
    subbed = ""
    for sec in bigram:
        r1, c1 = findrc(sec[0], key)
        r2, c2 = findrc(sec[1], key)

        if r1 == r2:
            subbed += key[r1][(c1 + 1) % 5]
            subbed += key[r1][(c2 + 1) % 5]
        elif c1 == c2:
            subbed += key[(r1 + 1) % 5][c1]
            subbed += key[(r2 + 1) % 5][c2]
        else:
            subbed += key[r1][c2]
            subbed += key[r2][c1]
    return subbed


def transmit(ciphertext, key):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
    s.bind(("127.0.0.1", port))
    s.listen(5)
    c, addr = s.accept()
    try:
        key_str = "|".join([",".join(row) for row in key])
        data = key_str + "||" + ciphertext
        c.sendall(data.encode())
    finally:
        c.close()
        # s.close()


if __name__ == "__main__":
    plaintxt = "attack"
    key = "monarchy"
    ckey = keygen(key)
    print("Key Matrix:")
    for i in ckey:
        print(i)
    ciphertext = encrypt(plaintxt, ckey)
    print(f"Plaintext: {plaintxt}")
    print(f"Ciphertext: {ciphertext}")
    transmit(ciphertext, ckey)
