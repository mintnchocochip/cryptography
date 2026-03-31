# vigenere

def vig_keygen(partial_key, plaintext):
    if not partial_key:
        return ""
    full_key = ""
    kp = 0
    for ch in plaintext:
        if ch.isalpha():
            k = partial_key[kp % len(partial_key)]
            full_key += k.lower() if ch.islower() else k.upper()
            kp += 1
        else:
            full_key += ch
    return full_key


def vig_encrypt(plaintext, partial_key):
    full_key = vig_keygen(partial_key, plaintext)
    ciphertxt = ""

    for i, ch in enumerate(plaintext):
        if not ch.isalpha():
            ciphertxt += ch
            continue

        k = full_key[i]
        if ch.islower():
            p = ord(ch) - ord("a")
            kk = ord(k.lower()) - ord("a")
            ciphertxt += chr(((p + kk) % 26) + ord("a"))
        else:
            p = ord(ch) - ord("A")
            kk = ord(k.upper()) - ord("A")
            ciphertxt += chr(((p + kk) % 26) + ord("A"))

    return ciphertxt


def vig_decrypt(ciphertext, key):
    plaintxt = ""
    aligned = len(key) == len(ciphertext)
    key_pos = 0

    for i, ch in enumerate(ciphertext):
        if not ch.isalpha():
            plaintxt += ch
            continue

        if aligned:
            k = key[i]
        else:
            k = key[key_pos] if key_pos < len(key) else "a"
            key_pos += 1

        if not k.isalpha():
            k = "a"

        if ch.islower():
            c = ord(ch) - ord("a")
            kk = ord(k.lower()) - ord("a")
            plaintxt += chr(((c - kk + 26) % 26) + ord("a"))
        else:
            c = ord(ch) - ord("A")
            kk = ord(k.upper()) - ord("A")
            plaintxt += chr(((c - kk + 26) % 26) + ord("A"))

    return plaintxt

#railfence
def rf_encrypt(plaintxt, depth):
    if len(plaintxt)%depth != 0:
        plaintxt += "*" *  (depth - (len(plaintxt) %depth))
    cipherlist = [[] for _ in range(depth)]
    c = 0
    for i in plaintxt:
        cipherlist[c % depth].append(i)
        c += 1
    cipherlist = ["".join(i) for i in cipherlist]
    return "".join(cipherlist)

def rf_decrypt(ciphertxt, depth):
    plaintxt = ""
    n = len(ciphertxt) // depth
    rows = []
    idx = 0
    for _ in range(depth):
        rows.append(ciphertext[idx:idx+n])
        idx += n
    for col in range(n):
        for row in range(depth):
            plaintxt += rows[row][col]
    return plaintxt.rstrip("*")


if __name__ == "__main__":
    plaintext = "hello world"
    partial_key = "whattawonderful"

    ciphertext = vig_encrypt(plaintext, partial_key)
    full_key = vig_keygen(partial_key, plaintext)
    decrypted = vig_decrypt(ciphertext, full_key)

    if plaintext == decrypted:
        print("vigenere works")
    else:
        print("vigenere failed")
        print("plaintext :", plaintext)
        print("ciphertext:", ciphertext)
        print("decrypted :", decrypted)
        # --- Railfence (row-slice) test ---
        rf_plain = "attack at dawn"
        depth = 4

        rf_cipher = rf_encrypt(rf_plain, depth)
        rf_dec = rf_decrypt(rf_cipher, depth)

        print("=== Railfence (row-slice) ===")
        print("plaintext :", rf_plain)
        print("depth     :", depth)
        print("ciphertext:", rf_cipher)
        print("decrypted :", rf_dec)
        print("result    :", "PASS" if rf_plain == rf_dec else "FAIL")
