from sqlalchemy import func
from sqlalchemy.orm import Session
from src import models

class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def create_order(
        self,
        user_id: int,
        origin_zip: str,
        destination_zip: str,
        weight: float,
        freight_type: models.FreightTypeEnum,
        distance_km: float,
        freight_value: float,
    ) -> models.Order:
        order = models.Order(
            user_id=user_id,
            origin_zip=origin_zip,
            destination_zip=destination_zip,
            weight=weight,
            freight_type=freight_type,
            distance_km=distance_km,
            freight_value=freight_value,
            status=models.OrderStatus.confirmed
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> models.Order | None:
        return self.db.query(models.Order).filter(models.Order.id == order_id).first()

    def list_by_user(self, user_id: int) -> list[models.Order]:
        return (
            self.db.query(models.Order)
            .filter(models.Order.user_id == user_id)
            .order_by(models.Order.created_at.desc())
            .all()
        )

    def count_orders_today(self) -> int:
        return (
            self.db.query(func.count(models.Order.id))
            .filter(func.date(models.Order.created_at) == func.current_date())
            .scalar()
        )