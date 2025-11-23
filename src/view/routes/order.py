from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .helpers import get_current_employee, get_current_user
from src.database import get_db
from src.model.order_repository import OrderRepository
from src.model.payment_repository import PaymentRepository
from src.view.schemas.order import OrderCreate
from src.view.schemas.payment import Payment
from src.domain.usecases.freight import FreightUseCases
from src.domain.usecases.order import OrderUseCases
from src.domain.usecases.payment import PaymentUseCase
from src.domain.entities.employees import JobRole

router = APIRouter(prefix="/orders")

@router.post("/")
async def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    usecase = OrderUseCases(OrderRepository(db), FreightUseCases())
    try:
        order = await usecase.create_order(current["user_id"], payload)
        return order
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/orders")
def list_my_orders(db: Session = Depends(get_db), current=Depends(get_current_user)):
    usecase = OrderUseCases(OrderRepository(db), FreightUseCases())
    return usecase.list_user_orders(current["user_id"])


@router.get("/orders/{order_id}/delivery")
def get_order_for_delivery(
    order_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    if current["job_role"] != JobRole.deliverer.value:
        raise HTTPException(403, "Not allowed")

    usecase = OrderUseCases(OrderRepository(db), FreightUseCases())
    try:
        return usecase.get_order_for_delivery(order_id)
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.get("/orders/count/today")
def count_orders_today(
    db: Session = Depends(get_db),
    current=Depends(get_current_employee),
):
    if current["job_role"] != JobRole.manager.value:
        raise HTTPException(403, "Only manager")

    usecase = OrderUseCases(OrderRepository(db), FreightUseCases())
    return { "count": usecase.count_orders_today() }

@router.post("/orders/{order_id}/pay")
def pay_order(order_id: int, payload: Payment, db: Session = Depends(get_db)):
    repo = PaymentRepository(db)
    usecase = PaymentUseCase(repo)
    try:
        result = usecase.process_payment(order_id, payload.method)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))