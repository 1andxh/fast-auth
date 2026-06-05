def test_password_gets_hashed():
    from src.auth.security import security

    password = "passpass"
    hashed_password = security.hash_password(password)

    assert password != hashed_password
    