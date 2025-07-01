from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql+psycopg2://user1:password@postgres:5433/employee_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Prediction(Base):
       __tablename__ = "predictions"
       id = Column(Integer, primary_key=True, index=True)
       features = Column(JSON)
       prediction = Column(Integer)
       source = Column(String)
       timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)