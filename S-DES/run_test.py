#!/usr/bin/env python3
"""
Simple test runner for S-DES server and client interaction
"""

import os
import subprocess
import sys
import threading
import time


def run_server():
    """Run the server with predefined inputs"""
    print("Starting S-DES Server...")

    # Prepare input for server
    inputs = "Hello\n1010000010\n"

    try:
        # Run server with input
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        stdout, stderr = process.communicate(input=inputs, timeout=10)

        print("Server Output:")
        print(stdout)
        if stderr:
            print("Server Errors:")
            print(stderr)

    except subprocess.TimeoutExpired:
        process.kill()
        print("Server process timed out")
    except Exception as e:
        print(f"Server error: {e}")


def run_client():
    """Run the client"""
    print("\nStarting S-DES Client...")
    time.sleep(2)  # Wait for server to start

    try:
        # Run client
        process = subprocess.Popen(
            [sys.executable, "client.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        stdout, stderr = process.communicate(timeout=10)

        print("Client Output:")
        print(stdout)
        if stderr:
            print("Client Errors:")
            print(stderr)

    except subprocess.TimeoutExpired:
        process.kill()
        print("Client process timed out")
    except Exception as e:
        print(f"Client error: {e}")


def test_manual_input():
    """Test with manual input"""
    print("=" * 60)
    print("MANUAL S-DES TEST")
    print("=" * 60)

    try:
        from client import decrypt_message
        from server import encrypt_message, generate_subkeys

        # Test data
        message = "ABC"
        key = "0110011001"

        print(f"Input Message: {message}")
        print(f"Key: {key}")

        # Generate subkeys
        key_bits = [int(bit) for bit in key]
        k1, k2 = generate_subkeys(key_bits)

        print(f"K1: {''.join(map(str, k1))}")
        print(f"K2: {''.join(map(str, k2))}")

        # Encrypt
        print("\nEncryption process:")
        cipher_text = encrypt_message(message, k1, k2)
        print(f"Cipher Text: {cipher_text}")

        # Decrypt
        print("\nDecryption process:")
        decrypted = decrypt_message(cipher_text, k1, k2)
        print(f"Decrypted Text: {decrypted}")

        # Verify
        print(f"\nVerification: {'PASS' if message == decrypted else 'FAIL'}")

    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Test error: {e}")


def main():
    """Main test function"""
    print("S-DES SERVER-CLIENT TEST RUNNER")
    print("=" * 60)

    # Test 1: Manual test
    test_manual_input()

    print("\n" + "=" * 60)
    print("NETWORK TEST (SERVER-CLIENT)")
    print("=" * 60)

    # Test 2: Network test
    # Start server in thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Start client in thread
    client_thread = threading.Thread(target=run_client)
    client_thread.daemon = True
    client_thread.start()

    # Wait for completion
    server_thread.join(timeout=15)
    client_thread.join(timeout=15)

    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

    print("\nTo run manually:")
    print("1. Open terminal 1: python server.py")
    print("2. Open terminal 2: python client.py")
    print("3. Enter message and key in server terminal")


if __name__ == "__main__":
    main()
