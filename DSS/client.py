import json
import socket
import sys

MASK64 = (1 << 64) - 1

def _rotr(x, n):
    return ((x >> n) | (x << (64 - n))) & MASK64

def _shr(x, n):
    return (x >> n) & MASK64

def _ch(x, y, z):
    return (x & y) ^ ((~x) & z)

def _maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def _bsig0(x):
    return _rotr(x, 28) ^ _rotr(x, 34) ^ _rotr(x, 39)

def _bsig1(x):
    return _rotr(x, 14) ^ _rotr(x, 18) ^ _rotr(x, 41)

def _ssig0(x):
    return _rotr(x, 1) ^ _rotr(x, 8) ^ _shr(x, 7)

def _ssig1(x):
    return _rotr(x, 19) ^ _rotr(x, 61) ^ _shr(x, 6)

K = [
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
    0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
    0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
    0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
    0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
    0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
    0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
    0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
    0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
    0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
    0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
    0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
    0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817,
]

def sha512_bytes(data: bytes) -> bytes:
    h = [
        0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
        0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
    ]

    bit_len = len(data) * 8
    data += b"\x80"
    while (len(data) % 128) != 112:
        data += b"\x00"
    data += (0).to_bytes(8, "big") + bit_len.to_bytes(8, "big")

    for off in range(0, len(data), 128):
        block = data[off:off+128]
        w = [0] * 80
        for i in range(16):
            w[i] = int.from_bytes(block[i*8:(i+1)*8], "big")
        for i in range(16, 80):
            w[i] = (_ssig1(w[i-2]) + w[i-7] + _ssig0(w[i-15]) + w[i-16]) & MASK64

        a,b,c,d,e,f,g,hh = h
        for i in range(80):
            t1 = (hh + _bsig1(e) + _ch(e,f,g) + K[i] + w[i]) & MASK64
            t2 = (_bsig0(a) + _maj(a,b,c)) & MASK64
            hh = g
            g = f
            f = e
            e = (d + t1) & MASK64
            d = c
            c = b
            b = a
            a = (t1 + t2) & MASK64

        h = [
            (h[0] + a) & MASK64, (h[1] + b) & MASK64, (h[2] + c) & MASK64, (h[3] + d) & MASK64,
            (h[4] + e) & MASK64, (h[5] + f) & MASK64, (h[6] + g) & MASK64, (h[7] + hh) & MASK64,
        ]

    return b"".join(x.to_bytes(8, "big") for x in h)

def sha512_int(data: bytes) -> int:
    return int.from_bytes(sha512_bytes(data), "big")

def inv_mod(a, m):
    return pow(a % m, -1, m)

def dsa_verify(p, q, g, y, message: str, r, s):
    if not (0 < r < q and 0 < s < q):
        return False, None, None, None

    hm = sha512_int(message.encode("utf-8"))
    w = inv_mod(s, q)
    u1 = (hm * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return (v == r), u1, u2, v

def recv_all(sock):
    buf = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        buf += part
    return buf

def _parse_args(argv):
    host = "127.0.0.1"
    port = 5050

    i = 1
    while i < len(argv):
        a = argv[i].lower()
        if a in ("--host", "-h"):
            host = argv[i + 1]
            i += 2
        elif a in ("--port", "-p"):
            port = int(argv[i + 1])
            i += 2
        else:
            raise SystemExit(
                "Usage:\n"
                "  python client.py [--host HOST] [--port PORT]\n"
                "Examples:\n"
                "  python client.py\n"
                "  python client.py --host 127.0.0.1 --port 5050"
            )
    return host, port

def main(host="127.0.0.1", port=5050):
    print(f"[client] connecting to {host}:{port} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        raw = recv_all(s)

    data = json.loads(raw.decode("utf-8"))
    p = int(data["p"]); q = int(data["q"]); g = int(data["g"]); y = int(data["y"])
    msg = data["message"]
    r = int(data["r"]); s_ = int(data["s"])

    print("\nReceived from Server: p,q,g,y,r,s,Message")
    print(msg)

    ok, u1, u2, v = dsa_verify(p, q, g, y, msg, r, s_)

    print("\nVerification:")
    if u1 is not None:
        print("u1:", u1)
        print("u2:", u2)
        print("v:", v)

    print(f"\nv (from Sender):{r}")
    if v is not None:
        print(f"v (Calculated):{v}")

    print("\nSuccessful Verified Signature" if ok else "\nIncorrect Signature !!!")

if __name__ == "__main__":
    host, port = _parse_args(sys.argv)
    main(host=host, port=port)
