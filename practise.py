SBOX = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76] * 16
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def keyperm(key_bytes):
    # 1. Turn the 16-byte key into four 4-byte words
    roundkeys = []
    for i in range(0, 16, 4):
        roundkeys.append(list(key_bytes[i:i+4])) 
        
    # 2. We need 44 words total for AES-128 (4 initial + 40 for 10 rounds)
    for i in range(4, 44):
        # Grab the previous word (temp)
        temp = roundkeys[i - 1][:]
        
        # If it's a multiple of 4, do the complex stuff to temp
        if i % 4 == 0:
            # RotWord (shift left by 1)
            temp = temp[1:] + temp[:1]
            
            # SubWord (S-Box)
            temp = [SBOX[b] for b in temp]
            
            # XOR first byte with RCON
            temp[0] ^= RCON[(i // 4) - 1]

        # Finally, XOR temp with word[i-4] byte-by-byte
        # (This handles both your 'if' and 'else' cases!)
        new_word = []
        for j in range(4):
            new_word.append(roundkeys[i - 4][j] ^ temp[j])
            
        roundkeys.append(new_word)
        
    return roundkeys
