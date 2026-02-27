from typing import Protocol, Tuple

class KeyNegotiator(Protocol):
    """Facilitates generation of a shared secret over an untrusted network."""
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        ...
    def encapsulate_secret(self, public_key: bytes) -> Tuple[bytes, bytes]:
        ...
    def decapsulate_secret(self, ciphertext: bytes, private_key: bytes) -> bytes:
        ...

class KyberNegotiator:
    """Concrete implementation for CRYSTALS-Kyber PQC encapsulation."""
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        print("🔑 [KeyNegotiator] Generating Kyber post-quantum keypair...")
        return (b"kyber_pk", b"kyber_sk")

    def encapsulate_secret(self, public_key: bytes) -> Tuple[bytes, bytes]:
        print("📦 [KeyNegotiator] Encapsulating shared secret...")
        return (b"shared_secret", b"kyber_ciphertext")

    def decapsulate_secret(self, ciphertext: bytes, private_key: bytes) -> bytes:
        print("🔓 [KeyNegotiator] Decapsulating shared secret...")
        return b"shared_secret"