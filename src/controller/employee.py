from typing import Optional
from src.controller.auth import AuthUseCases
from src.model.employee_point_repository import EmployeePointRepository
from src.model.employee_repository import EmployeeRepository
from src import models

class EmployeeUseCases:
    def __init__(self, employees_repo: EmployeeRepository, points_repo: EmployeePointRepository):
        self.employees_repo = employees_repo
        self.points_repo = points_repo

    def create_employee(self, name: str, job_role: models.JobRole, registry_number: str, password: str, phone: Optional[str] = None):
        existing = self.employees_repo.get_by_registry(registry_number)
        if existing:
            raise ValueError("Registry number already registered")

        hashed = AuthUseCases.hash_password(password)
        employee = self.employees_repo.create_employee(name=name, job_role=job_role, registry_number=registry_number, password_hash=hashed, phone=phone)
        return employee

    def login_employee(self, registry_number: str, password: str) -> str:
        employee = self.employees_repo.get_by_registry(registry_number)
        if not employee:
            raise ValueError("Invalid credentials")

        if not AuthUseCases.verify_password(password, str(employee.password)):
            raise ValueError("Invalid credentials")

        token_data = { "sub": employee.registry_number, "type": "employee", "employee_id": employee.id, "job_role": employee.job_role.value }
        token = AuthUseCases.generate_jwt(token_data)
        return token

    def register_point(self, employee_id: int, point_type: models.PointType):
        point = self.points_repo.add_point(employee_id=employee_id, point_type=point_type)
        return point

    def list_points(self, employee_id: int):
        return self.points_repo.list_points(employee_id)
