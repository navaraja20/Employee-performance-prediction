from pydantic import BaseModel

class EmployeeInput(BaseModel):
    age: int
    experience: int
    department: str
    education: str

class PredictionResponse(BaseModel):
    id: int
    age: int
    experience: int
    department: str
    education: str
    performance_score: float

    class Config:
        orm_mode = True
