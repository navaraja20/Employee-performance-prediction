from sqlalchemy.orm import Session
from models import Prediction

def save_prediction(db: Session, prediction: str, features: dict):
    db_prediction = Prediction(prediction=prediction, features=str(features))
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction
