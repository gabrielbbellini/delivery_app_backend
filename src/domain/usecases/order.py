from src.domain.usecases.freight import FreightUseCases
from src.model.order_repository import OrderRepository
from src.view.schemas.freight import FreightCalcRequest
from src.view.schemas.order import OrderCreate


class OrderUseCases:
    def __init__(self, orders_repo: OrderRepository, freight_usecases: FreightUseCases):
        self.orders_repo = orders_repo
        self.freight_usecases = freight_usecases

    async def create_order(self, user_id: int, payload: OrderCreate):
        freight_payload = FreightCalcRequest(
            origin_zip=payload.origin_zip,
            destination_zip=payload.destination_zip,
            weight=payload.weight,
            freight_type=payload.freight_type
        )

        quote = await self.freight_usecases.calculate_quote(freight_payload)
        distance_km = quote["distance_km"]
        price = quote["price"]

        order = self.orders_repo.create_order(
            user_id=user_id,
            origin_zip=payload.origin_zip,
            destination_zip=payload.destination_zip,
            weight=payload.weight,
            freight_type=payload.freight_type,
            distance_km=distance_km,
            freight_value=price
        )
        return order

    def list_user_orders(self, user_id: int):
        return self.orders_repo.list_by_user(user_id)

    def get_order_for_delivery(self, order_id: int):
        order = self.orders_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        sender = order.user
        return {
            "order_id": order.id,
            "origin_zip": order.origin_zip,
            "destination_zip": order.destination_zip,
            "sender_name": sender.name,
            "sender_phone": sender.phone,
        }

    def count_orders_today(self) -> int:
        return self.orders_repo.count_orders_today()
    