from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
import secrets

pasword_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
)


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return pasword_hasher.hash(password)

    @staticmethod
    def verify_password(hashed: str, plain: str) -> bool:
        try:
            return pasword_hasher.verify(hashed, plain)
        except (VerifyMismatchError, VerificationError):
            return False

    @staticmethod
    def generate_refresh_token() -> str:
        return secrets.token_urlsafe(32)
