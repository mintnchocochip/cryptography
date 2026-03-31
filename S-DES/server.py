import socket

P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
P4 = (2, 4, 3, 1)
IP = (2, 6, 3, 1, 4, 8, 5, 7)
IP_INV = (4, 1, 3, 5, 7, 2, 8, 6)
EP = (4, 1, 2, 3, 2, 3, 4, 1)
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]


def bits_to_int(bits):
    return int("".join(map(str, bits)), 2)


def int_to_bits(n, width):
    # fixed-width, MSB-first
    s = format(n, f"0{width}b")
    return list(map(int, s))


def permute(bits, table):
    return [bits[i - 1] for i in table]


def shift(bits, n):
    return bits[n:] + bits[:n]


def xor(bits_a, bits_b):
    return [a ^ b for a, b in zip(bits_a, bits_b)]


def bin_to_int(bits):
    return bits_to_int(bits)


def int_to_bin(value, width):
    return int_to_bits(value, width)


def sbox_lookup(bits, box):
    row = (bits[0] << 1) | bits[3]
    col = (bits[1] << 1) | bits[2]
    result = box[row][col]
    return int_to_bin(result, 2)


def fk(block, key):
    left = block[:4]
    right = block[4:]
    expanded = permute(right, EP)
    temp = xor(expanded, key)
    left_half = temp[:4]
    right_half = temp[4:]
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


def encrypt_block(char, k1, k2):
    bits = int_to_bin(ord(char), 8)
    ip = permute(bits, IP)
    print(f"IP: {''.join(map(str, ip))}")

    round1 = fk(ip, k1)
    print(f"Round 1: {''.join(map(str, round1))}")
    swapped = round1[4:] + round1[:4]

    round2 = fk(swapped, k2)
    print(f"Round 2: {''.join(map(str, round2))}")
    cipher = permute(round2, IP_INV)
    return "".join(map(str, cipher))


def encrypt_message(message, k1, k2):
    cipher = ""
    for ch in message:
        cipher += encrypt_block(ch, k1, k2)
    return cipher


def transmit_payload(key, cipher):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 65432))
    server.listen(1)
    connection, address = server.accept()
    payload = key + ":" + cipher
    connection.send(payload.encode())
    connection.close()
    server.close()


if __name__ == "__main__":
    message = input("Enter message: ")
    key = input("Enter 10-bit binary key: ")
    key_bits = [int(bit) for bit in key]
    k1, k2 = generate_subkeys(key_bits)
    k1_str = "".join(map(str, k1))
    k2_str = "".join(map(str, k2))
    print("Input:")
    print(f"Message/Plaintext: {message}")
    print(f"Key: {key}")
    print("Subkeys:")
    print(f"K1: {k1_str}")
    print(f"K2: {k2_str}")
    print("Intermediate Results (IP, Round 1, 2) in binary format:")
    cipher_text = encrypt_message(message, k1, k2)
    print(f"Print Cipher Text: {cipher_text}")
    print("Transmitting...")
    transmit_payload(key, cipher_text)
