#!/usr/bin/env python3
"""Test Basic Crypto Operations"""

def test_caesar():
    """Test Caesar cipher logic"""
    def caesar_encrypt(text, shift):
        result = ""
        for char in text.upper():
            if char.isalpha():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += char
        return result

    encrypted = caesar_encrypt("HELLO", 3)
    expected = "KHOOR"
    assert encrypted == expected, f"Expected {expected}, got {encrypted}"
    print("✅ Caesar cipher test passed")

def test_vigenere():
    """Test Vigenere cipher logic"""
    def vigenere_encrypt(text, key):
        result = ""
        key = key.upper()
        key_index = 0

        for char in text.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result += encrypted_char
                key_index += 1
            else:
                result += char
        return result

    encrypted = vigenere_encrypt("HELLO", "KEY")
    print(f"✅ Vigenere cipher test: HELLO -> {encrypted}")

if __name__ == "__main__":
    test_caesar()
    test_vigenere()
    print("🎉 All basic crypto tests passed!")
