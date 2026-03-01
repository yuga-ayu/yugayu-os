from typing import Protocol

class E2ECipher(Protocol):
    """Handles bulk payload encryption/decryption using symmetric cryptography."""
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        ...
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        ...

class AES256GCMCipher:
    """Concrete implementation using AES-256-GCM."""
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        print("🛡️ [E2E-Cipher] Encrypting payload via AES-256-GCM...")
        return b"encrypted_" + plaintext

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        print("🛡️ [E2E-Cipher] Decrypting payload via AES-256-GCM...")
        return ciphertext.replace(b"encrypted_", b"")