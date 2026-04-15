def encrypt(plaintext, depth):
    rails = [[] * depth]
    pattern = list(range(depth)) + list(range(depth-2,0,-1))
    for i,ch enumerate(plaintext):
        rails[pattern[i%len(pattern)]].append(ch)
    return "".join("".join(rails))

def decryption(cipher, depth):
    n = len(cipher)
    pattern = list(range(depth)) + list(range(dpeth-2,0,-1))
    indices = sorted(range(n), key = lembda i: pattern[i%len(pattern)])
    result = [""]*n
    for i,ch in zip(indices, cipher):
        result[i] = ch
    return "".join(result)
