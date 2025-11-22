from fastapi import APIRouter, Depends, HTTPException
from .helpers import get_current_employee
from src.database import get_db
import src.models as models
from sqlalchemy.orm import Session

from src.model.repositories import EmployeePointRepository, EmployeeRepository
from src.usecases import EmployeeUseCases

router = APIRouter(prefix="/employees")

@router.post("/register")
def register_employee(
    name: str,
    job_role: models.JobRole,
    registry_number: str,
    password: str,
    phone: str | None = None,
    db: Session = Depends(get_db)
):
    usecases = EmployeeUseCases(EmployeeRepository(), EmployeePointRepository())
    try:
        return usecases.create_employee(
            db,
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
    point_type: models.PointType,
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    usecases = EmployeeUseCases(EmployeeRepository(), EmployeePointRepository())

    return usecases.register_point(db, current["employee_id"], point_type)


@router.get("/employees/me/points")
def list_employee_points(
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    usecases = EmployeeUseCases(EmployeeRepository(), EmployeePointRepository())
    return usecases.list_points(db, current["employee_id"])

employeeRouter = router