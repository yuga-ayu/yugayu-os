import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def generate_wallet(ayu_name: str, lab_path: Path, custom_path: Path = None):
    """Generates an Ed25519 keypair (ML-DSA placeholder) for a new ayu or admin."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    
    wallet_data = {
        "ayu_id": ayu_name,
        "public_key": base64.b64encode(pub_bytes).decode('utf-8'),
        "private_key": base64.b64encode(priv_bytes).decode('utf-8') 
    }
    
    # Use the custom path if provided (for repo-level admin keys)
    if custom_path:
        wallet_path = custom_path
    else:
        wallet_path = lab_path / "ayus" / ayu_name / ".yugayu-identity"
        
    wallet_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(wallet_path, "w") as f:
        json.dump(wallet_data, f, indent=4)
        
def sign_payload(wallet_path: Path, payload: str) -> str:
    """Signs a command payload using the private key."""
    if not wallet_path.exists():
        raise FileNotFoundError(f"Wallet not found at {wallet_path}")
        
    with open(wallet_path, "r") as f:
        wallet = json.load(f)
        
    priv_bytes = base64.b64decode(wallet["private_key"])
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
    
    signature = private_key.sign(payload.encode('utf-8'))
    return base64.b64encode(signature).decode('utf-8')