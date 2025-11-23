from sqlalchemy.orm import Session
from src import models

class UserRepository:

    def __init__ (self, db: Session) -> None:
        self.db = db

    def create_user(self, name: str, phone: str | None, email: str, password_hash: str) -> models.User:
        user = models.User(
            name=name,
            phone=phone,
            email=email,
            password=password_hash
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> models.User | None:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def get_by_id(self, user_id: int) -> models.User | None:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def update_user(self, user_id: int, **kwargs) -> models.User:
        self.db.query(models.User).filter(models.User.id == user_id).update(kwargs) # type: ignore
        self.db.commit()
        return self.get_by_id(user_id)
