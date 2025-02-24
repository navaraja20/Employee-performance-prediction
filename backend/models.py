from sqlalchemy import Column, Integer, String, Float
from database import Base

class EmployeePerformance(Base):
    __tablename__ = "employee_performance"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    experience = Column(Integer)
    rating = Column(Float)
    predicted_performance = Column(Float)
