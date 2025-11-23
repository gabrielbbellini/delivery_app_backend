from typing import Dict, Any
from src import utils

class AuthUseCases:
    @staticmethod
    def hash_password(password: str) -> str:
        return utils.hash_password(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return utils.verify_password(plain, hashed)

    @staticmethod
    def generate_jwt(subject: Dict[str, Any]) -> str:
        return utils.create_access_token(subject)

    @staticmethod
    def decode_jwt(token: str) -> Dict[str, Any]:
        return utils.decode_token(token)
