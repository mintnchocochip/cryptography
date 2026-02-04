import socket
from typing import List, Tuple

S_BOX = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
         0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
         0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
         0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
         0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
         0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
         0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
         0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
         0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
         0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
         0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
         0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
         0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
         0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
         0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
         0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def gmul(a: int, b: int) -> int:
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a ^= 0x1B
        b >>= 1
    return p & 0xFF


def add_round_key(state: List[int], round_key: List[int]) -> List[int]:
    return [s ^ k for s, k in zip(state, round_key)]


def sub_bytes(state: List[int]) -> List[int]:
    return [S_BOX[b] for b in state]


def shift_rows(state: List[int]) -> List[int]:
    out = state[:]
    out[1], out[5], out[9], out[13] = state[5], state[9], state[13], state[1]
    out[2], out[6], out[10], out[14] = state[10], state[14], state[2], state[6]
    out[3], out[7], out[11], out[15] = state[15], state[3], state[7], state[11]
    return out


def mix_single_column(col: List[int]) -> List[int]:
    return [
        gmul(col[0], 2) ^ gmul(col[1], 3) ^ col[2] ^ col[3],
        col[0] ^ gmul(col[1], 2) ^ gmul(col[2], 3) ^ col[3],
        col[0] ^ col[1] ^ gmul(col[2], 2) ^ gmul(col[3], 3),
        gmul(col[0], 3) ^ col[1] ^ col[2] ^ gmul(col[3], 2),
    ]


def mix_columns(state: List[int]) -> List[int]:
    out = []
    for c in range(4):
        col = state[c * 4 : c * 4 + 4]
        out.extend(mix_single_column(col))
    return out


def rot_word(word: List[int]) -> List[int]:
    return word[1:] + word[:1]


def sub_word(word: List[int]) -> List[int]:
    return [S_BOX[b] for b in word]


def expand_key(key_bytes: List[int]) -> List[List[int]]:
    assert len(key_bytes) == 16, "Key must be 16 bytes for AES-128"
    words = [key_bytes[i : i + 4] for i in range(0, 16, 4)]
    for i in range(4, 44):
        temp = words[i - 1][:]
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[i // 4]
        new_word = [a ^ b for a, b in zip(words[i - 4], temp)]
        words.append(new_word)

    round_keys: List[List[int]] = []
    for r in range(11):
        round_key = []
        for w in words[r * 4 : r * 4 + 4]:
            round_key.extend(w)
        round_keys.append(round_key)
    return round_keys


def hex_state(state: List[int]) -> str:
    return "".join(f"{b:02X}" for b in state)


def bytes_from_hex(hex_str: str) -> List[int]:
    if len(hex_str) % 2 != 0:
        raise ValueError("Hex string length must be even")
    return [int(hex_str[i : i + 2], 16) for i in range(0, len(hex_str), 2)]


def pkcs7_pad(data: bytes) -> bytes:
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len]) * pad_len


def encrypt_block(
    block: List[int], round_keys: List[List[int]]
) -> Tuple[List[int], List[str]]:
    state = block[:]
    logs = [f"Plain Block: {hex_state(state)}"]

    state = add_round_key(state, round_keys[0])
    logs.append(f"Round 0 (AddRoundKey): {hex_state(state)}")

    for r in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[r])
        logs.append(
            f"Round {r} (SubBytes+ShiftRows+MixColumns+AddRoundKey): {hex_state(state)}"
        )

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])
    logs.append(f"Round 10 (SubBytes+ShiftRows+AddRoundKey): {hex_state(state)}")

    return state, logs


def encrypt_message(plaintext: str, key_hex: str) -> Tuple[str, List[str]]:
    key_bytes = bytes_from_hex(key_hex)
    round_keys = expand_key(key_bytes)

    padded = pkcs7_pad(plaintext.encode())
    cipher_bytes: List[int] = []
    logs: List[str] = []

    for i in range(0, len(padded), 16):
        block = list(padded[i : i + 16])
        cipher_block, block_logs = encrypt_block(block, round_keys)
        logs.extend([f"Block {i // 16} - {entry}" for entry in block_logs])
        cipher_bytes.extend(cipher_block)

    cipher_hex = "".join(f"{b:02X}" for b in cipher_bytes)
    return cipher_hex, logs


def transmit_payload(
    key_hex: str, cipher_hex: str, host: str = "127.0.0.1", port: int = 65432
) -> None:
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port} ...")
    connection, address = server.accept()
    payload = key_hex + ":" + cipher_hex
    connection.send(payload.encode())
    connection.close()
    server.close()



def main() -> None:
    message = input("Enter message: ")
    key_hex = input("Enter 128-bit key in hex (32 hex chars): ").strip()

    if len(key_hex) != 32 or any(ch not in "0123456789abcdefABCDEF" for ch in key_hex):
        print("Invalid key: must be 32 hex characters (128 bits).")
        return

    try:
        cipher_hex, logs = encrypt_message(message, key_hex)
    except ValueError as exc:
        print(f"Encryption failed: {exc}")
        return

    print("\nInput:")
    print(f"Message/Plaintext: {message}")
    print(f"Key (hex):         {key_hex}")
    print("\nIntermediate Results (Rounds 0..10) in HEX format:")
    for entry in logs:
        print(entry)

    print(f"\nCipher Text (hex): {cipher_hex}")
    print("Transmitting...")
    transmit_payload(key_hex, cipher_hex)
    print("Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()
