import math

A0, B0, C0, D0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

T = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]
S = [
    7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,
]

F = lambda B, C, D: (B & C) | (~B & D)
G = lambda B, C, D: (B & D) | (C & ~D)
H = lambda B, C, D: B ^ C ^ D
I = lambda B, C, D: C ^ (B | ~D)
left_rotate = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def preprocess(msg: bytes):
    original_len = len(msg) * 8
    padded = bytearray(msg)
    padded.append(0x80)
    
    while len(padded) % 64 != 56:
        padded.append(0)
        
    padded.extend(original_len.to_bytes(8, 'little'))
    
    blocks = []
    for i in range(0, len(padded), 64):
        chunk = padded[i : i + 64]
        words = [int.from_bytes(chunk[j : j + 4], 'little') for j in range(0, 64, 4)]
        blocks.append(words)
        
    return blocks

def md5(msg: bytes) -> str:
    A, B, C, D = A0, B0, C0, D0
    
    for block in preprocess(msg):
        a, b, c, d = A, B, C, D
        
        for i in range(64):
            if i < 16:   func, k = F(b, c, d), i
            elif i < 32: func, k = G(b, c, d), (5 * i + 1) % 16
            elif i < 48: func, k = H(b, c, d), (3 * i + 5) % 16
            else:        func, k = I(b, c, d), (7 * i) % 16

            temp = (func + a + block[k] + T[i]) & 0xFFFFFFFF
            a = d
            d = c
            c = b
            b = (b + left_rotate(temp, S[i])) & 0xFFFFFFFF

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    return ''.join(w.to_bytes(4, 'little').hex() for w in [A, B, C, D])

if __name__ == '__main__':
    print(f'MD5(hello) = {md5(b"hello")}')
