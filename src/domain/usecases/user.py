from typing import Dict, Any

from src.domain.usecases.auth import AuthUseCases
from src.model.user_repository import UserRepository
from src.view.schemas.login import UserLogin
from src.view.schemas.user import UserCreate, UserUpdate

class UserUseCases:
    def __init__(self, users_repo: UserRepository):
        self.users_repo = users_repo

    def create_user(self, payload: UserCreate):
        existing = self.users_repo.get_by_email(payload.email)
        if existing:
            raise ValueError("Email already registered")

        hashed = AuthUseCases.hash_password(payload.password)
        user = self.users_repo.create_user(name=payload.name, phone=payload.phone, email=payload.email, password_hash=hashed)
        return user

    def login_user(self, payload: UserLogin) -> str:
        user = self.users_repo.get_by_email(payload.email)
        if not user:
            raise ValueError("Invalid credentials")

        if not AuthUseCases.verify_password(payload.password, str(user.password)):
            raise ValueError("Invalid credentials")

        token_data = { "sub": user.email, "type": "user", "user_id": user.id }
        token = AuthUseCases.generate_jwt(token_data)
        return token

    def update_user(self, user_id: int, payload: UserUpdate):
        updates: Dict[str, Any] = {}
        if payload.name is not None:
            updates["name"] = payload.name
        if payload.phone is not None:
            updates["phone"] = payload.phone
        if payload.email is not None:
            other = self.users_repo.get_by_email(payload.email)
            if bool(other) and bool(other.id != user_id):
                raise ValueError("Email already in use")
            updates["email"] = payload.email
        if payload.password is not None:
            updates["password"] = AuthUseCases.hash_password(payload.password)

        if not updates:
            return self.users_repo.get_by_id(user_id)

        updated = self.users_repo.update_user(user_id, **updates)
        return updated