from sqlalchemy.orm import Session
from src import models

class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def create_employee(self, name: str, job_role: models.JobRole, registry_number: str, password_hash: str, phone: str | None = None) -> models.Employee:
        employee = models.Employee(
            name=name,
            job_role=job_role,
            registry_number=registry_number,
            password=password_hash,
            phone=phone
        )
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get_by_registry(self, registry_number: str) -> models.Employee | None:
        return self.db.query(models.Employee).filter(models.Employee.registry_number == registry_number).first()

    def get_by_id(self, employee_id: int) -> models.Employee | None:
        return self.db.query(models.Employee).filter(models.Employee.id == employee_id).first()

