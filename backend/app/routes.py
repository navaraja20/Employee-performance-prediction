from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from database import get_db
from models import EmployeePrediction
from prediction import predict_employee_performance
from dependencies import get_pagination
import pandas as pd
import io

router = APIRouter()

# ✅ Single Prediction API (Unchanged)
@router.post("/predict")
def predict(employee_data: dict, db: Session = Depends(get_db)):
    prediction = predict_employee_performance(employee_data)
    new_entry = EmployeePrediction(**employee_data, predicted_score=prediction)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"performance_score": prediction, "id": new_entry.id}


# ✅ Batch Predictions via CSV Upload
@router.post("/batch-predict")
def batch_predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read CSV
        contents = file.file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(contents))

        # Ensure necessary columns exist
        required_columns = {"age", "gender", "marital_status", "job_role", "department",
                            "business_travel", "years_at_company", "total_working_years",
                            "years_in_current_role", "years_since_last_promotion", "monthly_income",
                            "hourly_rate", "stock_option_level", "percent_salary_hike",
                            "job_satisfaction", "work_life_balance", "job_involvement",
                            "environment_satisfaction", "performance_rating", "overtime"}
        
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="Missing required columns in CSV")

        predictions = []
        for _, row in df.iterrows():
            data = row.to_dict()
            score = predict_employee_performance(data)
            data["predicted_score"] = score
            predictions.append(EmployeePrediction(**data))

        db.bulk_save_objects(predictions)
        db.commit()

        return {"message": "Batch predictions saved successfully", "total_predictions": len(predictions)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch Past Predictions with Filtering & Pagination
@router.get("/past-predictions")
def get_past_predictions(
    db: Session = Depends(get_db),
    job_role: str = Query(None),
    department: str = Query(None),
    performance_rating: int = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None),
    page: int = Query(1, alias="page"),
    page_size: int = Query(10, alias="page_size")
):
    query = db.query(EmployeePrediction)

    if job_role:
        query = query.filter(EmployeePrediction.job_role == job_role)
    if department:
        query = query.filter(EmployeePrediction.department == department)
    if performance_rating:
        query = query.filter(EmployeePrediction.performance_rating == performance_rating)
    if start_date and end_date:
        query = query.filter(EmployeePrediction.timestamp.between(start_date, end_date))

    # Pagination
    total, items = get_pagination(query, page, page_size)
    
    return {"total": total, "page": page, "page_size": page_size, "predictions": items}
