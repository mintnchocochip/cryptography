import random
from sympy import isprime
e = 65537

def generatePQ():
    p, q = 4, 4
    while not isprime(p):
        p = random.getrandbits(1024)
    while not isprime(q) or q == p:
        q = random.getrandbits(1024)
    return p, q

def generateKeys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    print("n = ", n)
    print("phi(n) = ", phi)
    print("e = ", e)
    print("d = ", d)
    return e, d, n

def encrypt(e, n, message):
    cipher_ints = []
    for ch in message:
        c = pow(ord(ch), e, n)
        cipher_ints.append(str(c))
    cipher = ",".join(cipher_ints)
    print("Encrypted: ", cipher)
    return cipher


def decrypt(d, n, cipher):
    plain_chars = []
    for part in cipher.split(","):
        if not part:
            continue
        m = pow(int(part), d, n)
        plain_chars.append(chr(m))
    plaintext = "".join(plain_chars)
    print("Decrypted: ", plaintext)
    return plaintext

def main() -> None:
    plaintext = input("Enter the message: ")
    p, q = generatePQ()
    print("P = ", p)
    print("Q = ", q)
    e_val, d, n = generateKeys(p, q)
    ciphertext = encrypt(e_val, n, plaintext)
    print("Encryption done....")
    plain = decrypt(d, n, ciphertext)
    print("Round-trip: ", plain)


if __name__ == "__main__":
    main()
