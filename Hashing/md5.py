import math

A0 = 0x67452301
B0 = 0xEFCDAB89
C0 = 0x98BADCFE
D0 = 0x10325476

T = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]

S = [
    7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,
]

def F(B, C, D): return (B & C) | (~B & D)
def G(B, C, D): return (B & D) | (C & ~D)
def H(B, C, D): return B ^ C ^ D
def I(B, C, D): return C ^ (B | ~D)

def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def preprocess(plaintext):
    msg = plaintext.encode('utf-8')
    original_len_bits = len(msg) * 8

    msg += b'\x80'
    while len(msg) % 64 != 56:
        msg += b'\x00'
    msg += original_len_bits.to_bytes(8, byteorder='little')

    blocks = []
    for i in range(0, len(msg), 64):
        chunk = msg[i : i + 64]
        words = [int.from_bytes(chunk[j : j + 4], byteorder='little') for j in range(0, 64, 4)]
        blocks.append(words)

    return blocks


def compress(block, A, B, C, D):
    a, b, c, d = A, B, C, D
    round_states = []

    for i in range(64):
        if i < 16:
            func = F(b, c, d);  k = i
        elif i < 32:
            func = G(b, c, d);  k = (5 * i + 1) % 16
        elif i < 48:
            func = H(b, c, d);  k = (3 * i + 5) % 16
        else:
            func = I(b, c, d);  k = (7 * i) % 16

        temp = (func + a + block[k] + T[i]) & 0xFFFFFFFF
        a    = d
        d    = c
        c    = b
        b    = (b + left_rotate(temp, S[i])) & 0xFFFFFFFF

        if i in (15, 31, 47, 63):
            round_states.append((a, b, c, d))

    A = (A + a) & 0xFFFFFFFF
    B = (B + b) & 0xFFFFFFFF
    C = (C + c) & 0xFFFFFFFF
    D = (D + d) & 0xFFFFFFFF

    return A, B, C, D, round_states


def produce_digest(A, B, C, D):
    return ''.join(w.to_bytes(4, byteorder='little').hex() for w in [A, B, C, D])


def md5(plaintext, label=""):
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    print(f"Number of characters : {len(plaintext)}")

    blocks = preprocess(plaintext)
    A, B, C, D = A0, B0, C0, D0

    for idx, block in enumerate(blocks):
        hex_words = ' '.join(f"{w:08X}" for w in block)
        print(f"\nBlock {idx + 1} : {hex_words}")

        A, B, C, D, round_states = compress(block, A, B, C, D)

        for r, (ra, rb, rc, rd) in enumerate(round_states, start=1):
            print(f"  Round {r} : A={ra:08X}  B={rb:08X}  C={rc:08X}  D={rd:08X}")

    digest = produce_digest(A, B, C, D)
    print(f"\nFinal Hash Value : {digest}")
    return digest


def gettest():
    test1 = input("Enter Test Case 1 (<56 characters) : ")
    assert len(test1) < 56,  f"Must be < 56 chars, got {len(test1)}"

    test2 = input("Enter Test Case 2 (=56 characters) : ")
    assert len(test2) == 56, f"Must be = 56 chars, got {len(test2)}"

    test3 = input("Enter Test Case 3 (>56 characters) : ")
    assert len(test3) > 56,  f"Must be > 56 chars, got {len(test3)}"

    return test1, test2, test3


def main():
    t1, t2, t3 = gettest()
    md5(t1, "Test Case 1  (<448 bits / <56 characters)")
    md5(t2, "Test Case 2  (=448 bits / =56 characters)")
    md5(t3, "Test Case 3  (>448 bits / >56 characters)")

if __name__ == "__main__":
    main()
