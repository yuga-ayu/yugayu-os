from yugayu.core.e2e_cipher import AES256GCMCipher

def test_aes_cipher_encrypt_decrypt():
    """Test the concrete AES-GCM implementation of the E2ECipher protocol."""
    cipher = AES256GCMCipher()
    key = b"ephemeral_session_key"
    plaintext = b"sensitive_tensor_data"
    
    # 1. Test Encryption
    ciphertext = cipher.encrypt(plaintext, key)
    assert ciphertext == b"encrypted_" + plaintext
    
    # 2. Test Decryption
    decrypted = cipher.decrypt(ciphertext, key)
    assert decrypted == plaintext