from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from . import models
from .model.repositories import (
    PaymentRepository,
    UserRepository,
    EmployeeRepository,
    OrderRepository,
    EmployeePointRepository
)
from .schemas import (
    UserCreate,
    UserUpdate,
    UserLogin,
    OrderCreate,
    FreightCalcRequest
)
from . import utils

# AUTH USECASES
class AuthUseCases:
    @staticmethod
    def hash_password(password: str) -> str:
        return utils.hash_password(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return utils.verify_password(plain, hashed)

    @staticmethod
    def generate_jwt(subject: Dict[str, Any]) -> str:
        return utils.create_access_token(subject)

    @staticmethod
    def decode_jwt(token: str) -> Dict[str, Any]:
        return utils.decode_token(token)


# USER USECASES
class UserUseCases:
    def __init__(self, users_repo: UserRepository):
        self.users_repo = users_repo

    def create_user(self, db: Session, payload: UserCreate):
        # check duplicate
        existing = self.users_repo.get_by_email(db, payload.email)
        if existing:
            raise ValueError("Email already registered")

        hashed = AuthUseCases.hash_password(payload.password)
        user = self.users_repo.create_user(db, name=payload.name, phone=payload.phone, email=payload.email, password_hash=hashed)
        return user

    def login_user(self, db: Session, payload: UserLogin) -> str:
        user = self.users_repo.get_by_email(db, payload.email)
        if not user:
            raise ValueError("Invalid credentials")

        if not AuthUseCases.verify_password(payload.password, user.password):
            raise ValueError("Invalid credentials")

        token_data = { "sub": user.email, "type": "user", "user_id": user.id }
        token = AuthUseCases.generate_jwt(token_data)
        return token

    def update_user(self, db: Session, user_id: int, payload: UserUpdate):
        updates: Dict[str, Any] = {}
        if payload.name is not None:
            updates["name"] = payload.name
        if payload.phone is not None:
            updates["phone"] = payload.phone
        if payload.email is not None:
            other = self.users_repo.get_by_email(db, payload.email)
            if other and other.id != user_id:
                raise ValueError("Email already in use")
            updates["email"] = payload.email
        if payload.password is not None:
            updates["password"] = AuthUseCases.hash_password(payload.password)

        if not updates:
            return self.users_repo.get_by_id(db, user_id)

        updated = self.users_repo.update_user(db, user_id, **updates)
        return updated


# EMPLOYEE USECASES
class EmployeeUseCases:
    def __init__(self, employees_repo: EmployeeRepository, points_repo: EmployeePointRepository):
        self.employees_repo = employees_repo
        self.points_repo = points_repo

    def create_employee(self, db: Session, name: str, job_role: models.JobRole, registry_number: str, password: str, phone: Optional[str] = None):
        existing = self.employees_repo.get_by_registry(db, registry_number)
        if existing:
            raise ValueError("Registry number already registered")

        hashed = AuthUseCases.hash_password(password)
        employee = self.employees_repo.create_employee(db, name=name, job_role=job_role, registry_number=registry_number, password_hash=hashed, phone=phone)
        return employee

    def login_employee(self, db: Session, registry_number: str, password: str) -> str:
        employee = self.employees_repo.get_by_registry(db, registry_number)
        if not employee:
            raise ValueError("Invalid credentials")

        if not AuthUseCases.verify_password(password, employee.password):
            raise ValueError("Invalid credentials")

        token_data = { "sub": employee.registry_number, "type": "employee", "employee_id": employee.id, "job_role": employee.job_role.value }
        token = AuthUseCases.generate_jwt(token_data)
        return token

    def register_point(self, db: Session, employee_id: int, point_type: models.PointType):
        point = self.points_repo.add_point(db, employee_id=employee_id, point_type=point_type)
        return point

    def list_points(self, db: Session, employee_id: int):
        return self.points_repo.list_points(db, employee_id)


# FREIGHT / GEOCODING USECASES
class FreightUseCases:
    def __init__(self):
        pass

    async def calculate_quote(self, payload: FreightCalcRequest) -> Dict[str, Any]:
        try:
            lat1, lon1 = await utils.get_coordinates_from_cep(payload.origin_zip)
            lat2, lon2 = await utils.get_coordinates_from_cep(payload.destination_zip)
        except Exception as e:
            raise ValueError(f"Failed to get coordinates: {e}")

        try:
            distance_km = await utils.get_distance_km(lat1, lon1, lat2, lon2)
        except Exception as e:
            raise ValueError(f"Distance calculation failed: {e}")

        try:
            price = utils.calculate_freight_price(distance_km=distance_km, weight=payload.weight, freight_type=payload.freight_type)
        except Exception as e:
            raise ValueError(f"Price calculation failed: {e}")

        return { "distance_km": round(distance_km, 2), "price": round(price, 2), "freight_type": payload.freight_type }


# ORDER USECASES
class OrderUseCases:
    def __init__(self, orders_repo: OrderRepository, freight_usecases: FreightUseCases):
        self.orders_repo = orders_repo
        self.freight_usecases = freight_usecases

    async def create_order(self, db: Session, user_id: int, payload: OrderCreate):
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
            db=db,
            user_id=user_id,
            origin_zip=payload.origin_zip,
            destination_zip=payload.destination_zip,
            weight=payload.weight,
            freight_type=payload.freight_type,
            distance_km=distance_km,
            freight_value=price
        )
        return order

    def list_user_orders(self, db: Session, user_id: int):
        return self.orders_repo.list_by_user(db, user_id)

    def get_order_for_delivery(self, db: Session, order_id: int):
        order = self.orders_repo.get_by_id(db, order_id)
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

    def count_orders_today(self, db: Session) -> int:
        return self.orders_repo.count_orders_today(db)
    
class PaymentUseCase:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    def process_payment(self, db: Session, order_id: int, method: models.PaymentMethod):
        self.payment_repo.confirm_payment(db, order_id)
        if method == models.PaymentMethod.pix:
            return { "message": "Pagamento via Pix confirmado" }
        elif method == models.PaymentMethod.credit_card:
            return { "message": "Pagamento via cartão de crédito aprovado" }
        elif method == models.PaymentMethod.debit_card:
            return { "message": "Pagamento via cartão de débito aprovado" }
        else:
            raise ValueError("Método de pagamento inválido")
