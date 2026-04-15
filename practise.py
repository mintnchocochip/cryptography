def blockify(message_bits):
    original_len = len(message_bits)
    
    # 1. Append the "1" bit
    padded = message_bits[:] + [1]
    
    # 2. Keep adding "0" bits until length % 512 == 448
    # This is exactly like the while loop in your md5.py!
    while len(padded) % 512 != 448:
        padded.append(0)
        
    # 3. Create the 64-bit binary length
    len_bin = bin(original_len)[2:].zfill(64)
    len_bits = [int(bit) for bit in len_bin]
    
    # 4. Append the length to reach a perfect multiple of 512
    padded.extend(len_bits)
    
    # 5. Chop into 512-bit blocks
    blocks = []
    for i in range(0, len(padded), 512):
        blocks.append(padded[i : i + 512])
        
    return blocks
