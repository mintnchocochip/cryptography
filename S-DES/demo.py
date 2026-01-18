#!/usr/bin/env python3
"""
Simple S-DES Client-Server Demo
This script demonstrates the complete S-DES encryption and decryption process
"""

import socket
import threading
import time

# S-DES Constants
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
P4 = (2, 4, 3, 1)
IP = (2, 6, 3, 1, 4, 8, 5, 7)
IP_INV = (4, 1, 3, 5, 7, 2, 8, 6)
EP = (4, 1, 2, 3, 2, 3, 4, 1)
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]


def permute(bits, table):
    return [bits[i - 1] for i in table]


def shift(bits, n):
    return bits[n:] + bits[:n]


def xor(bits_a, bits_b):
    return [a ^ b for a, b in zip(bits_a, bits_b)]


def bin_to_int(bits):
    value = 0
    for b in bits:
        value = (value << 1) | b
    return value


def int_to_bin(value, width):
    return [(value >> i) & 1 for i in range(width - 1, -1, -1)]


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


def decrypt_block(cipher_bits, k1, k2):
    ip = permute(cipher_bits, IP)
    print(f"IP: {''.join(map(str, ip))}")

    round1 = fk(ip, k2)
    print(f"Round 1: {''.join(map(str, round1))}")
    swapped = round1[4:] + round1[:4]

    round2 = fk(swapped, k1)
    print(f"Round 2: {''.join(map(str, round2))}")
    plaintext = permute(round2, IP_INV)
    return bin_to_int(plaintext)


def decrypt_message(cipher_text, k1, k2):
    message = ""
    for i in range(0, len(cipher_text), 8):
        cipher_block = cipher_text[i : i + 8]
        cipher_bits = [int(bit) for bit in cipher_block]
        char_code = decrypt_block(cipher_bits, k1, k2)
        message += chr(char_code)
    return message


def run_server():
    """Server function that encrypts and sends data"""
    print("=" * 60)
    print("S-DES SERVER (Sender - Implement Encryption)")
    print("=" * 60)

    message = "Hello"
    key = "1010000010"

    print("Input:")
    print(f"Message/Plaintext: {message}")
    print(f"Key: {key}")

    key_bits = [int(bit) for bit in key]
    k1, k2 = generate_subkeys(key_bits)
    k1_str = "".join(map(str, k1))
    k2_str = "".join(map(str, k2))

    print("Subkeys:")
    print(f"K1: {k1_str}")
    print(f"K2: {k2_str}")
    print("Intermediate Results (IP, Round 1, 2) in binary format:")

    cipher_text = encrypt_message(message, k1, k2)
    print(f"\nCipher Text: {cipher_text}")
    print("Transmitting to client...")

    # Start server socket
    try:
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 65432))
        server.listen(1)
        print("Server listening on port 65432...")

        connection, address = server.accept()
        payload = key + ":" + cipher_text
        connection.send(payload.encode())
        connection.close()
        server.close()
        print("Data sent successfully!")

    except Exception as e:
        print(f"Server error: {e}")


def run_client():
    """Client function that receives and decrypts data"""
    time.sleep(2)  # Wait for server to start

    print("\n" + "=" * 60)
    print("S-DES CLIENT (Receiver - Implement Decryption)")
    print("=" * 60)

    try:
        client = socket.socket()
        client.connect(("127.0.0.1", 65432))
        payload = client.recv(1024).decode()
        client.close()

        key, cipher_text = payload.split(":", 1)
        key_bits = [int(bit) for bit in key]
        k1, k2 = generate_subkeys(key_bits)

        k1_str = "".join(map(str, k1))
        k2_str = "".join(map(str, k2))

        print(f"Received Cipher Text: {cipher_text}")
        print("Subkeys:")
        print(f"K1: {k1_str}")
        print(f"K2: {k2_str}")
        print("Intermediate Results (IP, Round 1, 2) in binary format:")

        decrypted_message = decrypt_message(cipher_text, k1, k2)

        print(f"\nText after decryption: {decrypted_message}")

    except Exception as e:
        print(f"Client error: {e}")


def demo_standalone():
    """Standalone demo without networking"""
    print("=" * 60)
    print("S-DES STANDALONE DEMO")
    print("=" * 60)

    message = "Test"
    key = "1010000010"

    print("Input:")
    print(f"Message/Plaintext: {message}")
    print(f"Key: {key}")

    key_bits = [int(bit) for bit in key]
    k1, k2 = generate_subkeys(key_bits)
    k1_str = "".join(map(str, k1))
    k2_str = "".join(map(str, k2))

    print("\nSubkeys:")
    print(f"K1: {k1_str}")
    print(f"K2: {k2_str}")

    print("\nEncryption:")
    print("Intermediate Results (IP, Round 1, 2) in binary format:")
    cipher_text = encrypt_message(message, k1, k2)
    print(f"\nCipher Text: {cipher_text}")

    print("\nDecryption:")
    print("Intermediate Results (IP, Round 1, 2) in binary format:")
    decrypted_message = decrypt_message(cipher_text, k1, k2)
    print(f"\nDecrypted Message: {decrypted_message}")

    print(f"\nVerification:")
    print(f"Original:  {message}")
    print(f"Decrypted: {decrypted_message}")
    print(f"Match: {'✓' if message == decrypted_message else '✗'}")


def demo_client_server():
    """Demo with client-server communication"""
    print("\n" + "=" * 60)
    print("S-DES CLIENT-SERVER DEMO")
    print("=" * 60)

    # Start server in a thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Start client in a thread
    client_thread = threading.Thread(target=run_client)
    client_thread.daemon = True
    client_thread.start()

    # Wait for both to complete
    server_thread.join(timeout=10)
    client_thread.join(timeout=10)


def main():
    """Main demo function"""
    print("S-DES ENCRYPTION/DECRYPTION DEMO")
    print("=" * 60)

    # Run standalone demo
    demo_standalone()

    # Run client-server demo
    demo_client_server()

    print("\n" + "=" * 60)
    print("DEMO COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
