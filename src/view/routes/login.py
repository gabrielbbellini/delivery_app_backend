from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.model.employee_point_repository import EmployeePointRepository
from src.model.employee_repository import EmployeeRepository
from src.model.user_repository import UserRepository
from src.view.schemas.login import UserLogin
from src.control.employee import EmployeeUseCases
from src.control.user import UserUseCases

router = APIRouter()

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_usecases = UserUseCases(UserRepository(db))
    employee_usecases = EmployeeUseCases(EmployeeRepository(db), EmployeePointRepository(db))

    try:
        user_payload = UserLogin(email=form_data.username, password=form_data.password)
        token = user_usecases.login_user(user_payload)
        return { "access_token": token, "role": "user" }
    except ValueError:
        pass

    try:
        token = employee_usecases.login_employee(registry_number=form_data.username, password=form_data.password)
        return { "access_token": token, "role": "employee" }
    except ValueError:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")