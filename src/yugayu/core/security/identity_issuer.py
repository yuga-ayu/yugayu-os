import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

VALID_ROLES = ["maintainer", "admin", "guest", "ayu"]

def issue_identity(entity_id: str, role: str, custom_path: Path = None) -> Path:
    """
    [ID Issuer Department]
    Generates an Ed25519 keypair and assigns a rigid RBAC role.
    """
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role requested: {role}")

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
        "entity_id": entity_id,
        "role": role,
        "public_key": base64.b64encode(pub_bytes).decode('utf-8'),
        "private_key": base64.b64encode(priv_bytes).decode('utf-8') 
    }
    
    if custom_path:
        wallet_path = custom_path
    else:
        wallet_path = Path.home() / "yugayu-lab" / "ayus" / entity_id / ".yugayu-identity"
        
    wallet_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(wallet_path, "w") as f:
        json.dump(wallet_data, f, indent=4)
        
    return wallet_path