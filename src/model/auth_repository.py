from sqlalchemy.orm import Session
from model.employee_repository import EmployeeRepository
from model.user_repository import UserRepository
from src import models

class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_user_by_email(self, email: str) -> models.User | None:
        return UserRepository.get_by_email(self, email)

    def get_employee_by_registry(self, registry_number: str) -> models.Employee | None:
        return EmployeeRepository.get_by_registry(self, registry_number)