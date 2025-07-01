# api/database/crud.py
from .models import Prediction
from .db import SessionLocal

def save_prediction(dataframe, prediction):
    db = SessionLocal()
    try:
        record = Prediction(**dataframe.iloc[0].to_dict(), PredictionResult=str(prediction))
        db.add(record)
        db.commit()
    finally:
        db.close()

def get_all_predictions():
    db = SessionLocal()
    try:
        return db.query(Prediction).all()
    finally:
        db.close()
