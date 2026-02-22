from yugayu.core.iam import verify_identity

def test_verify_identity_stub():
    """
    Currently, the IAM stub should auto-approve (return True) 
    so it doesn't block OS development.
    """
    result = verify_identity()
    assert result is True
