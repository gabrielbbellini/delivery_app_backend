from sqlalchemy.orm import Session
from src.domain.entities.employees import Employee, JobRole

class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def create_employee(self, name: str, job_role: JobRole, registry_number: str, password_hash: str, phone: str | None = None) -> Employee:
        employee = Employee(
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

    def get_by_registry(self, registry_number: str) -> Employee | None:
        return self.db.query(Employee).filter(Employee.registry_number == registry_number).first()

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

