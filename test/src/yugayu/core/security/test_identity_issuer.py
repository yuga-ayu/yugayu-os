import json
import pytest
from yugayu.core.security.identity_issuer import issue_identity

def test_issue_identity_success(tmp_path):
    custom_path = tmp_path / "test-identity.json"
    
    # 1. Issue a maintainer identity
    result_path = issue_identity("test-dev", "maintainer", custom_path=custom_path)
    
    # 2. Assert file exists and contains expected RBAC structure
    assert result_path.exists()
    with open(result_path, "r") as f:
        data = json.load(f)
        
    assert data["entity_id"] == "test-dev"
    assert data["role"] == "maintainer"
    assert "public_key" in data
    assert "private_key" in data

def test_issue_identity_invalid_role(tmp_path):
    # Ensure the issuer blocks unrecognized roles
    with pytest.raises(ValueError, match="Invalid role requested: overlord"):
        issue_identity("test-dev", "overlord", custom_path=tmp_path / "fail.json")