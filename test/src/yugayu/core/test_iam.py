from yugayu.core.iam import verify_identity
from unittest.mock import patch

# We must mock Path.exists and sign_payload as well, so the function doesn't crash or exit early
@patch("yugayu.core.iam.Path.exists")
@patch("yugayu.core.iam.sign_payload")
@patch("yugayu.core.iam.verify_signature")
def test_verify_identity_calls_passport(mock_verify_sig, mock_sign, mock_exists):
    # 1. Trick the function into thinking the wallet file exists
    mock_exists.return_value = True
    
    # 2. Mock the signing process so it doesn't crash trying to read a missing file
    mock_sign.return_value = "dummy_signature_bytes"
    
    # 3. Mock the final verification to succeed
    mock_verify_sig.return_value = True
    
    result = verify_identity(ayu_name="test-agent", payload="test-payload")
    
    # Assert the passport verification was actually reached and called!
    mock_verify_sig.assert_called_once()
    assert result is True