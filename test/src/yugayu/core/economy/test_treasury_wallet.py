import pytest
import base64
from pathlib import Path
from yugayu.core.economy.treasury_wallet import generate_wallet, sign_payload

def test_generate_and_sign_wallet(tmp_path):
    """Test generating a PQC-placeholder wallet and signing a payload in a sandboxed tmp dir."""
    ayu_name = "test-economy-ayu"
    lab_path = tmp_path / "yugayu-lab"
    
    # 1. Generate the wallet
    generate_wallet(ayu_name, lab_path)
    
    wallet_file = lab_path / "ayus" / ayu_name / ".yugayu-identity"
    assert wallet_file.exists()
    
    # 2. Test signing a payload
    payload = "authorize_10_prana"
    signature = sign_payload(wallet_file, payload)
    
    assert isinstance(signature, str)
    assert len(signature) > 10  # Ensure a valid base64 signature was generated

def test_sign_payload_missing_wallet(tmp_path):
    """Ensure signing fails securely if the identity file is missing."""
    with pytest.raises(FileNotFoundError):
        sign_payload(tmp_path / "nonexistent.json", "test_payload")