from pydantic import BaseModel
from typing import Dict, List, Union  # ✅ Import Union

class PredictionRequest(BaseModel):
    features: Dict[str, Union[str, int, float]]  # ✅ Use Union instead of |

class BatchPredictionRequest(BaseModel):
    data: List[Dict[str, Union[str, int, float]]]  # ✅ Use Union for batch predictions
