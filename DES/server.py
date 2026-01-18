import socket
import threading

from client import decrypt, encrypt


class DESServer:
    def __init__(self, host="localhost", port=9999):
        self.host = host
        self.port = port

    def handle_client(self, client_socket, address):
        """Handle client connection"""
        print(f"Connection established with {address}")

        try:
            while True:
                # Receive operation type
                operation = client_socket.recv(1024).decode().strip()
                if not operation:
                    break

                if operation == "ENCRYPT":
                    # Receive plaintext and key
                    plaintext = client_socket.recv(1024).decode().strip()
                    key = client_socket.recv(1024).decode().strip()

                    print(f"\nServer received encryption request:")
                    print(f"Plaintext: {plaintext}")
                    print(f"Key: {key}")

                    # Encrypt
                    ciphertext = encrypt(plaintext, key)

                    # Send result
                    client_socket.send(ciphertext.encode())

                elif operation == "DECRYPT":
                    # Receive ciphertext and key
                    ciphertext = client_socket.recv(1024).decode().strip()
                    key = client_socket.recv(1024).decode().strip()

                    print(f"\nServer received decryption request:")
                    print(f"Ciphertext: {ciphertext}")
                    print(f"Key: {key}")

                    # Decrypt
                    plaintext = decrypt(ciphertext, key)

                    # Send result
                    client_socket.send(plaintext.encode())

        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {address} closed")

    def start(self):
        """Start the server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"DES Server listening on {self.host}:{self.port}")
            print("Waiting for client connections...")

            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()

        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            server_socket.close()


if __name__ == "__main__":
    print("=" * 50)
    print("DES CRYPTOGRAPHY SERVER")
    print("=" * 50)

    server = DESServer()
    server.start()
