import socket
import threading

IP = [
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    60,
    52,
    44,
    36,
    28,
    20,
    12,
    4,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    64,
    56,
    48,
    40,
    32,
    24,
    16,
    8,
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
]

FP = [
    40,
    8,
    48,
    16,
    56,
    24,
    64,
    32,
    39,
    7,
    47,
    15,
    55,
    23,
    63,
    31,
    38,
    6,
    46,
    14,
    54,
    22,
    62,
    30,
    37,
    5,
    45,
    13,
    53,
    21,
    61,
    29,
    36,
    4,
    44,
    12,
    52,
    20,
    60,
    28,
    35,
    3,
    43,
    11,
    51,
    19,
    59,
    27,
    34,
    2,
    42,
    10,
    50,
    18,
    58,
    26,
    33,
    1,
    41,
    9,
    49,
    17,
    57,
    25,
]

PC1 = [
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    60,
    52,
    44,
    36,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    28,
    20,
    12,
    4,
]

PC2 = [
    14,
    17,
    11,
    24,
    1,
    5,
    3,
    28,
    15,
    6,
    21,
    10,
    23,
    19,
    12,
    4,
    26,
    8,
    16,
    7,
    27,
    20,
    13,
    2,
    41,
    52,
    31,
    37,
    47,
    55,
    30,
    40,
    51,
    45,
    33,
    48,
    44,
    49,
    39,
    56,
    34,
    53,
    46,
    42,
    50,
    36,
    29,
    32,
]

DBox = [
    32,
    1,
    2,
    3,
    4,
    5,
    4,
    5,
    6,
    7,
    8,
    9,
    8,
    9,
    10,
    11,
    12,
    13,
    12,
    13,
    14,
    15,
    16,
    17,
    16,
    17,
    18,
    19,
    20,
    21,
    20,
    21,
    22,
    23,
    24,
    25,
    24,
    25,
    26,
    27,
    28,
    29,
    28,
    29,
    30,
    31,
    32,
    1,
]

Perm = [
    16,
    7,
    20,
    21,
    29,
    12,
    28,
    17,
    1,
    15,
    23,
    26,
    5,
    18,
    31,
    10,
    2,
    8,
    24,
    14,
    32,
    27,
    3,
    9,
    19,
    13,
    30,
    6,
    22,
    11,
    4,
    25,
]

sbox = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans


def text_to_binary(text):
    binary = ""
    for char in text:
        binary += format(ord(char), "08b")
    return binary


def binary_to_text(binary):
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i : i + 8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text


def binary_to_hex(binary):
    hex_str = ""
    for i in range(0, len(binary), 4):
        nibble = binary[i : i + 4]
        if len(nibble) == 4:
            hex_str += format(int(nibble, 2), "X")
    return hex_str


def hex_to_binary(hex_str):
    binary = ""
    for hex_char in hex_str:
        binary += format(int(hex_char, 16), "04b")
    return binary


def pad_text(text):
    padding_length = 8 - (len(text) % 8)
    return text + chr(padding_length) * padding_length


def unpad_text(text):
    if text:
        padding_length = ord(text[-1])
        return text[:-padding_length]
    return text


def permute(bits, table):
    return "".join(bits[i - 1] for i in table)


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def generate_subkeys(key):
    key_binary = text_to_binary(key[:8].ljust(8, "\0"))
    key_56 = permute(key_binary, PC1)
    left = key_56[:28]
    right = key_56[28:]
    subkeys = []
    for i in range(16):
        left = left_shift(left, SHIFTS[i])
        right = left_shift(right, SHIFTS[i])
        combined = left + right
        subkey = permute(combined, PC2)
        subkeys.append(subkey)
    return subkeys


def f_function(right, subkey):
    expanded = permute(right, DBox)
    xor_result = xor(expanded, subkey)
    s_output = ""
    for i in range(8):
        chunk = xor_result[i * 6 : (i + 1) * 6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        s_value = sbox[i][row][col]
        s_output += format(s_value, "04b")
    return permute(s_output, Perm)


def des_encrypt_block(plaintext, key):
    subkeys = generate_subkeys(key)
    permuted = permute(plaintext, IP)
    left = permuted[:32]
    right = permuted[32:]
    print(f"Intermediate Results:")
    print(f"IP: {binary_to_hex(permuted)}")
    for i in range(16):
        new_left = right
        f_output = f_function(right, subkeys[i])
        new_right = xor(left, f_output)
        left, right = new_left, new_right
        if i < 3 or i == 15:
            print(f"Round {i + 1}: L={binary_to_hex(left)}, R={binary_to_hex(right)}")
        elif i == 3:
            print("...")
    combined = right + left
    return permute(combined, FP)


def des_decrypt_block(ciphertext, key):
    subkeys = generate_subkeys(key)
    subkeys.reverse()
    permuted = permute(ciphertext, IP)
    left = permuted[:32]
    right = permuted[32:]
    print(f"Intermediate Results:")
    print(f"IP: {binary_to_hex(permuted)}")
    for i in range(16):
        new_left = right
        f_output = f_function(right, subkeys[i])
        new_right = xor(left, f_output)
        left, right = new_left, new_right
        if i < 3 or i == 15:
            print(f"Round {i + 1}: L={binary_to_hex(left)}, R={binary_to_hex(right)}")
        elif i == 3:
            print("...")
    combined = right + left
    return permute(combined, FP)


def encrypt(plaintext, key):
    print(f"\n=== DES ENCRYPTION ===")
    print(f"Input Message/Plaintext: {plaintext}")
    print(f"Key: {key}")
    padded_text = pad_text(plaintext)
    ciphertext_binary = ""
    for i in range(0, len(padded_text), 8):
        block = padded_text[i : i + 8]
        block_binary = text_to_binary(block)
        encrypted_block = des_encrypt_block(block_binary, key)
        ciphertext_binary += encrypted_block
    ciphertext_hex = binary_to_hex(ciphertext_binary)
    print(f"\nCipher Text (HEX): {ciphertext_hex}")
    return ciphertext_hex


def decrypt(ciphertext_hex, key):
    print(f"\n=== DES DECRYPTION ===")
    print(f"Received Cipher Text (HEX): {ciphertext_hex}")
    ciphertext_binary = hex_to_binary(ciphertext_hex)
    plaintext_binary = ""
    for i in range(0, len(ciphertext_binary), 64):
        block = ciphertext_binary[i : i + 64]
        decrypted_block = des_decrypt_block(block, key)
        plaintext_binary += decrypted_block
    plaintext = binary_to_text(plaintext_binary)
    plaintext = unpad_text(plaintext)
    print(f"\nText after decryption: {plaintext}")
    return plaintext


class DESClient:
    def __init__(self, host="localhost", port=9999):
        self.host = host
        self.port = port

    def connect(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print(f"Connected to DES Server at {self.host}:{self.port}")
            while True:
                print("\n" + "=" * 50)
                print("DES Cryptography Client")
                print("=" * 50)
                print("1. Encrypt Message")
                print("2. Decrypt Message")
                print("3. Exit")
                print("=" * 50)
                choice = input("Enter your choice (1-3): ").strip()
                if choice == "1":
                    plaintext = input("Enter message to encrypt: ")
                    key = input("Enter 8-character key: ")
                    if len(key) != 8:
                        print(
                            "Warning: Key should be 8 characters. It will be padded or truncated."
                        )
                    client_socket.send("ENCRYPT".encode())
                    client_socket.send(plaintext.encode())
                    client_socket.send(key.encode())
                    ciphertext = client_socket.recv(1024).decode()
                    print(f"\nEncrypted message (HEX): {ciphertext}")
                elif choice == "2":
                    ciphertext = input("Enter ciphertext (HEX): ")
                    key = input("Enter 8-character key: ")
                    if len(key) != 8:
                        print(
                            "Warning: Key should be 8 characters. It will be padded or truncated."
                        )
                    client_socket.send("DECRYPT".encode())
                    client_socket.send(ciphertext.encode())
                    client_socket.send(key.encode())
                    plaintext = client_socket.recv(1024).decode()
                    print(f"\nDecrypted message: {plaintext}")
                elif choice == "3":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


def demo_des():
    print("=" * 70)
    print("DES ENCRYPTION/DECRYPTION DEMO")
    print("=" * 70)
    plaintext = "Cryptography"
    key = "Security"
    print(f"Demo with:")
    print(f"Message: {plaintext}")
    print(f"Key: {key}")
    print("\nSender (Implement Encryption)")
    print("Input:")
    print(f"Message/Plaintext: {plaintext}")
    print(f"Key: {key}")
    ciphertext = encrypt(plaintext, key)
    print("\n" + "=" * 50)
    print("Receiver (Implement Decryption)")
    decrypted_text = decrypt(ciphertext, key)
    print(f"\n" + "=" * 70)
    print(f"VERIFICATION:")
    print(f"Original:  {plaintext}")
    print(f"Decrypted: {decrypted_text}")
    print(f"Match: {'✓' if plaintext == decrypted_text else '✗'}")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "client":
            client = DESClient()
            client.connect()
        elif sys.argv[1] == "demo":
            demo_des()
        else:
            print("Usage:")
            print("  python client.py client    # Connect to server")
            print("  python client.py demo      # Run demo")
    else:
        demo_des()
