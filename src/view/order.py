from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .helpers import get_current_employee, get_current_user
from src.database import get_db
import src.models as models
from src.model.repositories import OrderRepository, PaymentRepository
from src.schemas import OrderCreate, Payment
from src.usecases import FreightUseCases, OrderUseCases, PaymentUseCase

router = APIRouter(prefix="/orders")

@router.post("/")
async def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    usecase = OrderUseCases(OrderRepository(), FreightUseCases())
    try:
        order = await usecase.create_order(db, current["user_id"], payload)
        return order
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/orders")
def list_my_orders(db: Session = Depends(get_db), current=Depends(get_current_user)):
    usecase = OrderUseCases(OrderRepository(), FreightUseCases())
    return usecase.list_user_orders(db, current["user_id"])


@router.get("/orders/{order_id}/delivery")
def get_order_for_delivery(
    order_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    if current["job_role"] != models.JobRole.deliverer.value:
        raise HTTPException(403, "Not allowed")

    usecase = OrderUseCases(OrderRepository(), FreightUseCases())
    try:
        return usecase.get_order_for_delivery(db, order_id)
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.get("/orders/count/today")
def count_orders_today(
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    if current["job_role"] != models.JobRole.manager.value:
        raise HTTPException(403, "Only manager")

    usecase = OrderUseCases(OrderRepository(), FreightUseCases())
    return { "count": usecase.count_orders_today(db) }

@router.post("/orders/{order_id}/pay")
def pay_order(order_id: int, payload: Payment, db: Session = Depends(get_db)):
    repo = PaymentRepository()
    usecase = PaymentUseCase(repo)
    try:
        result = usecase.process_payment(db, order_id, payload.method)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
