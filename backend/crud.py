from sqlalchemy.orm import Session
import models, schemas

def create_employee_performance(db: Session, employee: schemas.EmployeePerformanceCreate, predicted_score: float):
    db_employee = models.EmployeePerformance(
        name=employee.name,
        experience=employee.experience,
        rating=employee.rating,
        predicted_performance=predicted_score
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.EmployeePerformance).offset(skip).limit(limit).all()
