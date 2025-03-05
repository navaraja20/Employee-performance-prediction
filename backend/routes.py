from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.prediction import predict_performance
from app.models import EmployeePrediction

router = APIRouter()

@router.post("/predict")
def make_prediction(employee_data: dict, db: Session = Depends(get_db)):
    predicted_score = predict_performance(employee_data)

    # Save prediction to database
    prediction_entry = EmployeePrediction(**employee_data, predicted_score=predicted_score)
    db.add(prediction_entry)
    db.commit()
    db.refresh(prediction_entry)

    return {"performance_score": predicted_score}

@router.get("/past-predictions")
def get_past_predictions(db: Session = Depends(get_db)):
    predictions = db.query(EmployeePrediction).all()
    return predictions
