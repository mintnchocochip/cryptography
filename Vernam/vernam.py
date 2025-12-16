def generate_key(length):
    key = []
    for i in range(length):
        key.append(i % 256)
    return key


def encrypt(plaintext, key):
    if len(plaintext) != len(key):
        return None
    ciphertext = []
    for i in range(len(plaintext)):
        ciphertext.append(ord(plaintext[i]) ^ key[i])
    return ciphertext


def decrypt(ciphertext, key):
    if len(ciphertext) != len(key):
        return None
    plaintext = []
    for i in range(len(ciphertext)):
        plaintext.append(chr(ciphertext[i] ^ key[i]))
    return "".join(plaintext)


def encrypt_bytes(data, key):
    if len(data) != len(key):
        return None
    result = []
    for i in range(len(data)):
        result.append(data[i] ^ key[i])
    return result


def decrypt_bytes(data, key):
    if len(data) != len(key):
        return None
    result = []
    for i in range(len(data)):
        result.append(data[i] ^ key[i])
    return result


def text_to_bytes(text):
    return [ord(c) for c in text]


def bytes_to_text(data):
    return "".join(chr(b) for b in data)


class VernamCipher:
    def __init__(self):
        pass

    def generate_random_key(self, length):
        key = []
        seed = 12345
        for i in range(length):
            seed = (seed * 1103515245 + 12345) % (2**31)
            key.append(seed % 256)
        return key

    def encrypt_text(self, plaintext, key=None):
        if key is None:
            key = self.generate_random_key(len(plaintext))
        return encrypt(plaintext, key), key

    def decrypt_text(self, ciphertext, key):
        return decrypt(ciphertext, key)

    def encrypt_data(self, data, key=None):
        if key is None:
            key = self.generate_random_key(len(data))
        return encrypt_bytes(data, key), key

    def decrypt_data(self, ciphertext, key):
        return decrypt_bytes(ciphertext, key)
