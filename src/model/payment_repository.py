import datetime
from sqlalchemy.orm import Session
from src.domain.entities.order import Order

class PaymentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def confirm_payment(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError("Pedido não encontrado")

        order.paid_at = datetime.datetime.now(datetime.timezone.utc) # type: ignore
        self.db.commit()
        self.db.refresh(order)
        return
