from pydantic import BaseModel

class PredictionInput(BaseModel):
    Age: float
    BusinessTravel: str
    Department: str
    Education: int
    Gender: str
    HourlyRate: float
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: float
    OverTime: str
    TotalWorkingYears: float
    WorkLifeBalance: int
    YearsAtCompany: float
    YearsInCurrentRole: float
    YearsSinceLastPromotion: float