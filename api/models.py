from sqlalchemy import Column, Integer, String, Float
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    education = Column(String, nullable=False)
    performance_score = Column(Float, nullable=False)
