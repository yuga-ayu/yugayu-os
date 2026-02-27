# src/yugayu/core/passport.py
import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

def verify_signature(wallet_path: Path, payload: str, signature_b64: str) -> bool:
    """The Hub validates the cryptographic signature of the ayu."""
    try:
        if not wallet_path.exists():
            return False
            
        with open(wallet_path, "r") as f:
            wallet = json.load(f)
            
        pub_bytes = base64.b64decode(wallet["public_key"])
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
        signature = base64.b64decode(signature_b64)
        
        public_key.verify(signature, payload.encode('utf-8'))
        return True
    except (InvalidSignature, KeyError, ValueError):
        return False