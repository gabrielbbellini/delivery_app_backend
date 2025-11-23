from sqlalchemy.orm import Session
from src.domain.entities.user import User

class UserRepository:

    def __init__ (self, db: Session) -> None:
        self.db = db

    def create_user(self, name: str, phone: str | None, email: str, password_hash: str) -> User:
        user = User(
            name=name,
            phone=phone,
            email=email,
            password=password_hash
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, **kwargs) -> User:
        self.db.query(User).filter(User.id == user_id).update(kwargs) # type: ignore
        self.db.commit()
        return self.get_by_id(user_id)
