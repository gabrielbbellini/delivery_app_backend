import datetime
from sqlalchemy.orm import Session
from src import models

class PaymentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def confirm_payment(self, order_id: int):
        order = self.db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise ValueError("Pedido não encontrado")

        order.paid_at = datetime.datetime.now(datetime.timezone.utc) # type: ignore
        self.db.commit()
        self.db.refresh(order)
        return
