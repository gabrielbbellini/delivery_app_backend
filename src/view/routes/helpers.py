from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.domain.usecases.auth import AuthUseCases

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = AuthUseCases.decode_jwt(token)
        if payload.get("type") != "user":
            raise Exception("Not a user token")
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_employee(token: str = Depends(oauth2_scheme)):
    try:
        payload = AuthUseCases.decode_jwt(token)
        if payload.get("type") != "employee":
            raise Exception("Not an employee token")
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired employee token",
        )
