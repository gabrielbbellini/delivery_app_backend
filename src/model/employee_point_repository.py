from sqlalchemy.orm import Session
from src.domain.entities.employee_point import PointType, EmployeePoint

class EmployeePointRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_point(self, employee_id: int, point_type: PointType):
        point = EmployeePoint(
            employee_id=employee_id,
            point_type=point_type
        )
        self.db.add(point)
        self.db.commit()
        self.db.refresh(point)
        return point

    def list_points(self, employee_id: int) -> list[EmployeePoint]:
        return (
            self.db.query(EmployeePoint)
            .filter(EmployeePoint.employee_id == employee_id)
            .order_by(EmployeePoint.timestamp.desc())
            .all()
        )