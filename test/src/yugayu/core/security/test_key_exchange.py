from yugayu.core.security.key_exchange import KyberNegotiator

def test_kyber_negotiator_flow():
    """Test the concrete Kyber implementation of the KeyNegotiator protocol."""
    negotiator = KyberNegotiator()
    
    # 1. Generate Keypair
    pk, sk = negotiator.generate_keypair()
    assert pk == b"kyber_pk"
    assert sk == b"kyber_sk"
    
    # 2. Encapsulate Secret
    shared_secret, ciphertext = negotiator.encapsulate_secret(pk)
    assert shared_secret == b"shared_secret"
    assert ciphertext == b"kyber_ciphertext"
    
    # 3. Decapsulate Secret
    decapsulated = negotiator.decapsulate_secret(ciphertext, sk)
    assert decapsulated == shared_secret