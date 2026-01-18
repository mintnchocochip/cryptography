#!/usr/bin/env python3
"""
Test script for S-DES client-server communication
This script demonstrates the complete S-DES encryption and decryption process
"""

import os
import socket
import subprocess
import sys
import threading
import time

# Add current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client import decrypt_message
from server import encrypt_message, generate_subkeys, int_to_bin


def test_sdes_direct():
    """Test S-DES encryption and decryption directly without network"""
    print("=" * 70)
    print("S-DES DIRECT TEST")
    print("=" * 70)

    # Test data
    message = "Hello"
    key = "1010000010"

    print(f"Input:")
    print(f"Message/Plaintext: {message}")
    print(f"Key: {key}")

    # Generate subkeys
    key_bits = [int(bit) for bit in key]
    k1, k2 = generate_subkeys(key_bits)

    k1_str = "".join(map(str, k1))
    k2_str = "".join(map(str, k2))

    print(f"\nSubkeys:")
    print(f"K1: {k1_str}")
    print(f"K2: {k2_str}")

    print(f"\nEncryption process:")
    print("Intermediate Results (IP, Round 1, 2) in binary format:")

    # Encrypt
    cipher_text = encrypt_message(message, k1, k2)
    print(f"\nCipher Text: {cipher_text}")

    print(f"\nDecryption process:")
    print("Intermediate Results (IP, Round 1, 2) in binary format:")

    # Decrypt
    decrypted_message = decrypt_message(cipher_text, k1, k2)
    print(f"\nDecrypted Message: {decrypted_message}")

    # Verify
    print(f"\n" + "=" * 70)
    print(f"VERIFICATION:")
    print(f"Original:  {message}")
    print(f"Decrypted: {decrypted_message}")
    print(f"Match: {'✓' if message == decrypted_message else '✗'}")
    print("=" * 70)


def run_server_test():
    """Run server with predefined input"""
    import server

    # Mock input for server
    original_input = __builtins__["input"]
    inputs = iter(["Hello", "1010000010"])
    __builtins__["input"] = lambda prompt="": next(inputs)

    try:
        # Run server main
        message = "Hello"
        key = "1010000010"
        key_bits = [int(bit) for bit in key]
        k1, k2 = server.generate_subkeys(key_bits)
        k1_str = "".join(map(str, k1))
        k2_str = "".join(map(str, k2))

        print("S-DES SERVER")
        print("=" * 50)
        print("Input:")
        print(f"Message/Plaintext: {message}")
        print(f"Key: {key}")
        print("Subkeys:")
        print(f"K1: {k1_str}")
        print(f"K2: {k2_str}")
        print("Intermediate Results (IP, Round 1, 2) in binary format:")

        cipher_text = server.encrypt_message(message, k1, k2)
        print(f"Print Cipher Text: {cipher_text}")
        print("Transmitting...")

        # Start server
        server.transmit_payload(key, cipher_text)

    finally:
        __builtins__["input"] = original_input


def run_client_test():
    """Run client test"""
    time.sleep(1)  # Wait for server to start
    from client import main as client_main

    print("\nS-DES CLIENT")
    print("=" * 50)
    client_main()


def test_client_server():
    """Test complete client-server communication"""
    print("=" * 70)
    print("S-DES CLIENT-SERVER TEST")
    print("=" * 70)

    # Start server in a thread
    server_thread = threading.Thread(target=run_server_test)
    server_thread.daemon = True
    server_thread.start()

    # Start client in a thread
    client_thread = threading.Thread(target=run_client_test)
    client_thread.daemon = True
    client_thread.start()

    # Wait for both to complete
    server_thread.join(timeout=5)
    client_thread.join(timeout=5)


def test_multiple_messages():
    """Test with different messages and keys"""
    print("\n" + "=" * 70)
    print("S-DES MULTIPLE TEST CASES")
    print("=" * 70)

    test_cases = [
        ("A", "0000000000"),
        ("Hi", "1111111111"),
        ("Test", "1010101010"),
        ("SDES", "0110011001"),
        ("123", "1001100110"),
    ]

    for i, (message, key) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Message: '{message}', Key: '{key}'")

        # Generate subkeys
        key_bits = [int(bit) for bit in key]
        k1, k2 = generate_subkeys(key_bits)

        # Encrypt
        cipher_text = encrypt_message(message, k1, k2)
        print(f"Cipher: {cipher_text}")

        # Decrypt
        decrypted = decrypt_message(cipher_text, k1, k2)
        print(f"Decrypted: '{decrypted}'")
        print(f"Match: {'✓' if message == decrypted else '✗'}")


def main():
    """Run all tests"""
    print("S-DES IMPLEMENTATION TEST SUITE")
    print("=" * 70)

    # Test 1: Direct encryption/decryption
    test_sdes_direct()

    # Test 2: Multiple test cases
    test_multiple_messages()

    # Test 3: Client-server communication
    try:
        test_client_server()
    except Exception as e:
        print(f"Client-server test failed: {e}")

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
