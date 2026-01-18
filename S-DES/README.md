# S-DES (Simplified Data Encryption Standard) Implementation

A complete Python implementation of the Simplified Data Encryption Standard (S-DES) algorithm with client-server architecture for secure communication.

## Features

- **Complete S-DES Implementation**: Full 8-bit block cipher with 10-bit key
- **Encryption & Decryption**: Both operations with detailed intermediate results
- **Client-Server Architecture**: Network-based secure communication
- **Binary Output Format**: All results displayed in binary format
- **Step-by-step Process**: Shows IP, Round 1, and Round 2 intermediate results
- **Comprehensive Testing**: Multiple test cases and verification

## Files

- `server.py` - S-DES server that encrypts messages and transmits them
- `client.py` - S-DES client that receives and decrypts messages
- `demo.py` - Complete demonstration with both standalone and client-server modes
- `test_sdes.py` - Comprehensive test suite
- `run_test.py` - Test runner for server-client interaction
- `README.md` - This documentation file

## Requirements

- Python 3.6 or higher
- Standard Python libraries only (no external dependencies)

## Usage

### 1. Server-Client Mode

#### Start the Server
```bash
python server.py
```

Enter the message and 10-bit binary key when prompted:
- Message: Any text string (e.g., "Hello")
- Key: 10-bit binary string (e.g., "1010000010")

#### Start the Client
In a separate terminal:
```bash
python client.py
```

The client will automatically receive and decrypt the message from the server.

### 2. Demo Mode

Run the complete demonstration:
```bash
python demo.py
```

This shows both standalone and client-server functionality.

### 3. Run Tests

```bash
python test_sdes.py
```

Runs comprehensive tests with multiple message and key combinations.

## Sample Input/Output

### Server (Sender - Implement Encryption)

```
Input:
Message/Plaintext: Hello
Key: 1010000010

Subkeys:
K1: 10100100
K2: 01000011

Intermediate Results (IP, Round 1, 2) in binary format:
IP: 10000010
Round 1: 00000010
Round 2: 10110000
IP: 11100100
Round 1: 10100100
Round 2: 10111010
IP: 11100010
Round 1: 01100010
Round 2: 01000110
IP: 11100010
Round 1: 01100010
Round 2: 01000110
IP: 11100111
Round 1: 01110111
Round 2: 01100111

Cipher Text: 1110000011111000000011010000110100101111
```

### Client (Receiver - Implement Decryption)

```
Received Cipher Text: 1110000011111000000011010000110100101111

Subkeys:
K1: 10100100
K2: 01000011

Intermediate Results (IP, Round 1, 2) in binary format:
IP: 10110000
Round 1: 00100000
Round 2: 10000010
IP: 10111010
Round 1: 01001010
Round 2: 11100100
IP: 01000110
Round 1: 00100110
Round 2: 11100010
IP: 01000110
Round 1: 00100110
Round 2: 11100010
IP: 01100111
Round 1: 01110111
Round 2: 11100111

Decrypted Message: Hello
```

## Algorithm Details

### S-DES Components

1. **Key Generation**:
   - P10 permutation: (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
   - P8 permutation: (6, 3, 7, 4, 8, 5, 10, 9)
   - Left shifts: 1 bit for K1, then 2 more bits for K2

2. **Encryption Process**:
   - Initial Permutation (IP): (2, 6, 3, 1, 4, 8, 5, 7)
   - Two rounds with Feistel function
   - Final Permutation (IP⁻¹): (4, 1, 3, 5, 7, 2, 8, 6)

3. **Feistel Function**:
   - Expansion Permutation (EP): (4, 1, 2, 3, 2, 3, 4, 1)
   - S-Box substitutions (S0 and S1)
   - P4 permutation: (2, 4, 3, 1)

4. **Decryption**:
   - Same process as encryption but with subkeys in reverse order (K2, then K1)

### Key Features

- **8-bit Block Size**: Processes data in 8-bit blocks
- **10-bit Key Size**: Uses 10-bit encryption keys
- **Binary Format**: All intermediate results shown in binary
- **Network Communication**: TCP socket communication between server and client

## API Reference

### Core Functions

- `generate_subkeys(key_bits)` - Generates K1 and K2 from 10-bit key
- `encrypt_block(char, k1, k2)` - Encrypts a single character
- `encrypt_message(message, k1, k2)` - Encrypts entire message
- `decrypt_block(cipher_bits, k1, k2)` - Decrypts a single block
- `decrypt_message(cipher_text, k1, k2)` - Decrypts entire message

### Helper Functions

- `permute(bits, table)` - Apply permutation according to table
- `shift(bits, n)` - Left circular shift by n positions
- `xor(bits_a, bits_b)` - XOR two bit arrays
- `sbox_lookup(bits, box)` - S-box substitution
- `fk(block, key)` - Feistel function

## Testing

The implementation includes comprehensive tests:

1. **Direct Encryption/Decryption**: Tests core algorithm functionality
2. **Multiple Messages**: Tests with various message types and lengths
3. **Different Keys**: Tests with different 10-bit binary keys
4. **Client-Server Communication**: Tests network functionality
5. **Edge Cases**: Tests boundary conditions

## Example Usage

```python
from server import generate_subkeys, encrypt_message
from client import decrypt_message

# Test data
message = "Test"
key_bits = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]

# Generate subkeys
k1, k2 = generate_subkeys(key_bits)

# Encrypt
cipher = encrypt_message(message, k1, k2)
print(f"Cipher: {cipher}")

# Decrypt
decrypted = decrypt_message(cipher, k1, k2)
print(f"Decrypted: {decrypted}")
```

## Network Protocol

The client-server communication uses a simple protocol:
1. Server encrypts message and creates payload: `key:ciphertext`
2. Server sends payload via TCP socket
3. Client receives payload and splits key and ciphertext
4. Client decrypts using the received key

## Security Notes

⚠️ **Educational Purpose**: This is a simplified version of DES for educational purposes only. S-DES is not secure for real-world applications due to its small key size and block size.

For production use, consider:
- AES (Advanced Encryption Standard)
- Modern authenticated encryption schemes
- Proper key management practices

## Troubleshooting

### Common Issues

1. **Key Format**: Ensure the key is exactly 10 bits (0s and 1s only)
2. **Connection Issues**: Make sure server is running before starting client
3. **Port in Use**: Change port number if 65432 is occupied

### Error Messages

- "Invalid key": Key must be exactly 10 binary digits
- "Connection error": Server may not be running or port is blocked
- "No connection could be made": Check if server is listening

## License

This implementation is provided for educational purposes. Feel free to use and modify according to your needs.