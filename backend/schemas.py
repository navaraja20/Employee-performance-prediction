from pydantic import BaseModel

class EmployeePerformanceCreate(BaseModel):
    name: str
    experience: int
    rating: float

class EmployeePerformanceResponse(EmployeePerformanceCreate):
    id: int
    predicted_performance: float

    class Config:
        orm_mode = True
