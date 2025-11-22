from fastapi import APIRouter, FastAPI
from .database import engine, Base
from . import models 
from .view import freight, login, user, employee, order

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Frete API - Desafio Técnico")

apiRouter = APIRouter(prefix="/api")
apiRouter.include_router(freight.router)
apiRouter.include_router(login.router)
apiRouter.include_router(user.router)
apiRouter.include_router(employee.router)
apiRouter.include_router(order.router)

app.include_router(apiRouter)