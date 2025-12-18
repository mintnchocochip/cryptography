import socket


def decrypt(string, key):
    plaintxt = ""

    if not key:
        return string
    aligned = len(key) == len(string)
    key_pos = 0
    for i, ch in enumerate(string):
        if not ch.isalpha():
            plaintxt += ch
            continue

        if aligned:
            k = key[i]
        else:
            k = key[key_pos] if key_pos < len(key) else "a"
            key_pos += 1

        if not k.isalpha():
            k = "a"

        if ch.islower():
            k = k.lower()
            plaintxt += chr(((ord(ch) - ord(k) + 26) % 26) + ord("a"))
        else:
            k = k.upper()
            plaintxt += chr(((ord(ch) - ord(k) + 26) % 26) + ord("A"))
    return plaintxt


def receive():
    s = socket.socket()
    port = 8080
    s.connect(("127.0.0.1", port))

    data = b""
    while True:
        part = s.recv(1024)
        if not part:
            break
        data += part
    s.close()

    parts = data.decode().splitlines()
    if not parts:
        return ("", "")
    key = parts[0].strip()

    txt = parts[1] if len(parts) > 1 else ""
    return (key, txt)


if __name__ == "__main__":
    key, ciphertxt = receive()
    plaintxt = decrypt(ciphertxt, key)
    print("Received: " + ciphertxt)
    print("Decrypted: " + plaintxt)
