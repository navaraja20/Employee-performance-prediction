from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    prediction = Column(String, nullable=False)
    features = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
