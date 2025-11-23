from fastapi import APIRouter, Depends, HTTPException
from .helpers import get_current_employee
from src.database import get_db
from sqlalchemy.orm import Session
from src.domain.entities.employees import JobRole
from src.domain.entities.employee_point import PointType
from src.model.employee_point_repository import EmployeePointRepository
from src.model.employee_repository import EmployeeRepository
from src.domain.usecases.employee import EmployeeUseCases

router = APIRouter(prefix="/employees")

@router.post("/register")
def register_employee(
    name: str,
    job_role: JobRole,
    registry_number: str,
    password: str,
    phone: str | None = None,
    db: Session = Depends(get_db)
):
    usecases = EmployeeUseCases(EmployeeRepository(db), EmployeePointRepository(db))
    try:
        return usecases.create_employee(
            name=name,
            job_role=job_role,
            registry_number=registry_number,
            password=password,
            phone=phone,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/employees/me/point")
def register_employee_point(
    point_type: PointType,
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    usecases = EmployeeUseCases(EmployeeRepository(db), EmployeePointRepository(db))

    return usecases.register_point(current["employee_id"], point_type)


@router.get("/employees/me/points")
def list_employee_points(
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    usecases = EmployeeUseCases(EmployeeRepository(db), EmployeePointRepository(db))
    return usecases.list_points(current["employee_id"])

employeeRouter = router