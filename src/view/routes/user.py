from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .helpers import get_current_user
from src.database import get_db
from src.model.user_repository import UserRepository
from src.view.schemas.user import UserCreate, UserUpdate
from src.controller.user import UserUseCases

router = APIRouter(prefix="/users")

@router.post("/register")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    usecases = UserUseCases(UserRepository(db))

    try:
        user = usecases.create_user(payload)
        return { "message": "User created", "user": user }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/me")
def update_user(payload: UserUpdate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    usecases = UserUseCases(UserRepository(db))
    try:
        return usecases.update_user(current["user_id"], payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))