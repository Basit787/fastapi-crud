import jwt

from app.auth.security import create_access_token
from app.auth.security import decode_access_token
from app.auth.security import hash_password
from app.auth.security import verify_password
from lib.settings import JWT_ALGORITHM
from lib.settings import JWT_SECRET_KEY


def test_hash_and_verify_password():
    hashed = hash_password("secret")

    assert hashed != "secret"
    assert verify_password("secret", hashed)
    assert not verify_password("wrong", hashed)


def test_create_and_decode_access_token():
    token = create_access_token(42)
    payload = decode_access_token(token)

    assert payload["sub"] == "42"
    assert "exp" in payload


def test_decode_invalid_token_raises():
    try:
        decode_access_token("invalid.token.value")
        raised = False
    except jwt.PyJWTError:
        raised = True

    assert raised


def test_token_uses_configured_algorithm():
    token = create_access_token(1)
    header = jwt.get_unverified_header(token)

    assert header["alg"] == JWT_ALGORITHM


def test_token_signed_with_secret():
    token = create_access_token(7)
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

    assert payload["sub"] == "7"
