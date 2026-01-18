import socket

P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
P4 = (2, 4, 3, 1)
IP = (2, 6, 3, 1, 4, 8, 5, 7)
IP_INV = (4, 1, 3, 5, 7, 2, 8, 6)
EP = (4, 1, 2, 3, 2, 3, 4, 1)
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]


def permute(bits, table):
    return [bits[index - 1] for index in table]


def shift(bits, n):
    return bits[n:] + bits[:n]


def xor(bits_a, bits_b):
    return [a ^ b for a, b in zip(bits_a, bits_b)]


def bin_to_int(bits):
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def int_to_bin(value, width):
    return [(value >> i) & 1 for i in range(width - 1, -1, -1)]


def sbox_lookup(bits, box):
    row = (bits[0] << 1) | bits[3]
    col = (bits[1] << 1) | bits[2]
    return int_to_bin(box[row][col], 2)


def fk(block, key):
    left = block[:4]
    right = block[4:]
    expanded = permute(right, EP)
    mixed = xor(expanded, key)
    left_half = mixed[:4]
    right_half = mixed[4:]
    s0_out = sbox_lookup(left_half, S0)
    s1_out = sbox_lookup(right_half, S1)
    p4_out = permute(s0_out + s1_out, P4)
    return xor(left, p4_out) + right


def generate_subkeys(key_bits):
    p10_key = permute(key_bits, P10)
    left = p10_key[:5]
    right = p10_key[5:]
    left = shift(left, 1)
    right = shift(right, 1)
    k1 = permute(left + right, P8)
    left = shift(left, 2)
    right = shift(right, 2)
    k2 = permute(left + right, P8)
    return k1, k2


def decrypt_block(block_bits, k1, k2):
    ip = permute(block_bits, IP)
    print(f"IP: {''.join(map(str, ip))}")

    round1 = fk(ip, k2)
    print(f"Round 1: {''.join(map(str, round1))}")
    swapped = round1[4:] + round1[:4]

    round2 = fk(swapped, k1)
    print(f"Round 2: {''.join(map(str, round2))}")
    plain_bits = permute(round2, IP_INV)
    return chr(bin_to_int(plain_bits))


def decrypt_cipher(cipher_text, k1, k2):
    plaintext = ""
    for index in range(0, len(cipher_text), 8):
        block = cipher_text[index : index + 8]
        block_bits = [int(bit) for bit in block]
        plaintext += decrypt_block(block_bits, k1, k2)
    return plaintext


def receive_payload():
    client = socket.socket()
    client.connect(("127.0.0.1", 65432))
    payload = client.recv(1024).decode()
    client.close()
    key, cipher_text = payload.split(":")
    return key, cipher_text


if __name__ == "__main__":
    key_string, cipher_string = receive_payload()
    key_bits = [int(bit) for bit in key_string]
    k1, k2 = generate_subkeys(key_bits)
    k1_string = "".join(map(str, k1))
    k2_string = "".join(map(str, k2))
    print(f"Received Cipher Text: {cipher_string}")
    print("Subkeys:")
    print(f"K1: {k1_string}")
    print(f"K2: {k2_string}")
    print("Intermediate Results (IP, Round 1, 2) in binary format:")
    plaintext = decrypt_cipher(cipher_string, k1, k2)
    print(f"Text after decryption: {plaintext}")
