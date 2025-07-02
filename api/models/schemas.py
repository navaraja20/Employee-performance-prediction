# api/models/schemas.py

from pydantic import BaseModel

class PredictionRequest(BaseModel):
    Age: int
    Gender: str
    JobRole: str
    JobSatisfaction: int
    MonthlyIncome: float
