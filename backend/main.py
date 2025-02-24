from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud, database
import joblib

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Load trained ML model
model = joblib.load("models/model.pkl")

@app.post("/predict/", response_model=schemas.EmployeePerformanceResponse)
def predict_performance(employee: schemas.EmployeePerformanceCreate, db: Session = Depends(database.get_db)):
    features = [[employee.experience, employee.rating]]
    predicted_score = model.predict(features)[0]
    return crud.create_employee_performance(db, employee, predicted_score)

@app.get("/employees/")
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_employees(db, skip, limit)
