# api/database/crud.py
from .models import Prediction
from .db import SessionLocal

def save_prediction(dataframe, prediction):
    db = SessionLocal()
    try:
        # convert all values to native Python types (e.g., int, float, str)
        input_dict = {
            k: (v.item() if hasattr(v, 'item') else v)
            for k, v in dataframe.iloc[0].to_dict().items()
        }
        record = Prediction(**input_dict, PredictionResult=int(prediction))
        db.add(record)
        db.commit()
    finally:
        db.close()

def get_predictions():
    db = SessionLocal()
    try:
        return db.query(Prediction).all()
    finally:
        db.close()
