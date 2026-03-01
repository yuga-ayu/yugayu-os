from unittest.mock import patch
from yugayu.core.security.identity_verifier import Ed25519Bouncer

@patch("yugayu.core.security.identity_verifier.Path.exists")
def test_verify_identity_checks_wallet(mock_exists):
    # Setup the bouncer class
    bouncer = Ed25519Bouncer()
    
    # 1. Test when the wallet file DOES NOT exist
    mock_exists.return_value = False
    result_fail = bouncer.verify_identity(ayu_name="test-agent", payload=b"test", signature=b"sig")
    assert result_fail is False
    
    # 2. Test when the wallet file DOES exist
    mock_exists.return_value = True
    result_success = bouncer.verify_identity(ayu_name="test-agent", payload=b"test", signature=b"sig")
    assert result_success is True