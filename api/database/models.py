# api/database/models.py

from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    Age = Column(Integer)
    Gender = Column(String)
    JobRole = Column(String)
    JobSatisfaction = Column(Integer)
    MonthlyIncome = Column(Float)
    PredictionResult = Column(Integer)
