from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.model.repositories import EmployeePointRepository, EmployeeRepository, UserRepository
from src.schemas import UserLogin
from src.usecases import EmployeeUseCases, UserUseCases

router = APIRouter()

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_usecases = UserUseCases(UserRepository())
    employee_usecases = EmployeeUseCases(EmployeeRepository(), EmployeePointRepository())

    try:
        user_payload = UserLogin(email=form_data.username, password=form_data.password)
        token = user_usecases.login_user(db, user_payload)
        return { "access_token": token, "role": "user" }
    except ValueError:
        pass

    try:
        token = employee_usecases.login_employee(db, registry_number=form_data.username, password=form_data.password)
        return { "access_token": token, "role": "employee" }
    except ValueError:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")