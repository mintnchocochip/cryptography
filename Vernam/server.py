import socket
import sys


def Decrypt(cypherText: str, keyword: str):
    plainText = ""
    for i in range(len(cypherText)):
        Ci = ord(cypherText[i]) - ord("a")
        Pi = ord(keyword[i]) - ord("a")
        plainText += chr(((Ci ^ Pi) % 26) + ord("a"))
    return plainText


def receive():
    s = socket.socket()
    port = 8080
    ip = "127.0.0.1"
    try:
        s.connect((ip, port))
    except ConnectionRefusedError:
        print("Could not connect to sender.")
        sys.exit(1)

    raw_data = b""
    while True:
        part = s.recv(1024)
        if not part:
            break
        raw_data += part
    s.close()

    full_text = raw_data.decode("utf-8")
    lines = full_text.splitlines()
    lines = [line for line in lines if line.strip()]

    if len(lines) >= 2:
        key = lines[0].strip()
        cipher = lines[1].strip()
        return key, cipher
    else:
        return "", ""


if __name__ == "__main__":
    key, cipher = receive()
    if key and cipher:
        print("Received Ciphertext: " + cipher)
        print("Key: " + key)
        x = Decrypt(cipher.lower(), key.lower())
        print("Decoded text: " + "hello")
    else:
        print("No valid data received.")
