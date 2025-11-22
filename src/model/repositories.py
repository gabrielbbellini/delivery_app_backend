import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models

# User Repository
class UserRepository:

    @staticmethod
    def create_user(db: Session, name: str, phone: str, email: str, password_hash: str) -> models.User:
        user = models.User(
            name=name,
            phone=phone,
            email=email,
            password=password_hash
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_email(db: Session, email: str) -> models.User | None:
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> models.User | None:
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> models.User:
        db.query(models.User).filter(models.User.id == user_id).update(kwargs)
        db.commit()
        return UserRepository.get_by_id(db, user_id)


# Employee Repository (Managers and Deliverers)
class EmployeeRepository:

    @staticmethod
    def create_employee(db: Session, name: str, job_role: models.JobRole, registry_number: str, password_hash: str, phone: str | None = None) -> models.Employee:
        employee = models.Employee(
            name=name,
            job_role=job_role,
            registry_number=registry_number,
            password=password_hash,
            phone=phone
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    @staticmethod
    def get_by_registry(db: Session, registry_number: str) -> models.Employee | None:
        return db.query(models.Employee).filter(models.Employee.registry_number == registry_number).first()

    @staticmethod
    def get_by_id(db: Session, employee_id: int) -> models.Employee | None:
        return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


# Order Repository
class OrderRepository:

    @staticmethod
    def create_order(
        db: Session,
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
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_by_id(db: Session, order_id: int) -> models.Order | None:
        return db.query(models.Order).filter(models.Order.id == order_id).first()

    @staticmethod
    def list_by_user(db: Session, user_id: int) -> list[models.Order]:
        return (
            db.query(models.Order)
            .filter(models.Order.user_id == user_id)
            .order_by(models.Order.created_at.desc())
            .all()
        )

    @staticmethod
    def count_orders_today(db: Session) -> int:
        return (
            db.query(func.count(models.Order.id))
            .filter(func.date(models.Order.created_at) == func.current_date())
            .scalar()
        )
    
# Employee Points Repository
class EmployeePointRepository:

    @staticmethod
    def add_point(db: Session, employee_id: int, point_type: models.PointType):
        point = models.EmployeePoint(
            employee_id=employee_id,
            point_type=point_type
        )
        db.add(point)
        db.commit()
        db.refresh(point)
        return point

    @staticmethod
    def list_points(db: Session, employee_id: int) -> list[models.EmployeePoint]:
        return (
            db.query(models.EmployeePoint)
            .filter(models.EmployeePoint.employee_id == employee_id)
            .order_by(models.EmployeePoint.timestamp.desc())
            .all()
        )


# Auth / Login Repository
class AuthRepository:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> models.User | None:
        return UserRepository.get_by_email(db, email)

    @staticmethod
    def get_employee_by_registry(db: Session, registry_number: str) -> models.Employee | None:
        return EmployeeRepository.get_by_registry(db, registry_number)

class PaymentRepository:

    @staticmethod
    def confirm_payment(db: Session, order_id: int):
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise ValueError("Pedido não encontrado")

        order.paid_at = datetime.datetime.now(datetime.timezone.utc)
        db.commit()
        db.refresh(order)
        return
