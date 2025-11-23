from sqlalchemy.orm import Session
from src import models

class EmployeePointRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def add_point(self, employee_id: int, point_type: models.PointType):
        point = models.EmployeePoint(
            employee_id=employee_id,
            point_type=point_type
        )
        self.db.add(point)
        self.db.commit()
        self.db.refresh(point)
        return point

    def list_points(self, employee_id: int) -> list[models.EmployeePoint]:
        return (
            self.db.query(models.EmployeePoint)
            .filter(models.EmployeePoint.employee_id == employee_id)
            .order_by(models.EmployeePoint.timestamp.desc())
            .all()
        )