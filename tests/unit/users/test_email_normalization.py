def test_normalize_email():
    from src.users.utils import normalize_email

    unnormalized = " joHn@doE.com"
    normalized = normalize_email(unnormalized)

    assert normalized == "john@doe.com"
    assert normalize_email("JOHN.DOE@EXAMPLE.COM") == "john.doe@example.com"
