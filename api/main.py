from fastapi import FastAPI, HTTPException
from models import PredictionInput
from database import SessionLocal, Prediction
from ml_model import preprocess_data, load_model
from datetime import datetime

app = FastAPI()
model = load_model()

@app.post("/predict")
async def predict(data: list[PredictionInput], source: str = "webapp"):
       try:
           data_dict = [item.dict() for item in data]
           df = preprocess_data(data_dict)
           predictions = model.predict(df)
           results = []
           with SessionLocal() as session:
               for i, pred in enumerate(predictions):
                   prediction_entry = Prediction(features=data_dict[i], prediction=int(pred), source=source)
                   session.add(prediction_entry)
                   results.append({"features": data_dict[i], "prediction": int(pred)})
               session.commit()
           return results
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

@app.get("/past-predictions")
async def past_predictions(start_date: str, end_date: str, source: str = "all"):
       try:
           start = datetime.strptime(start_date, "%Y-%m-%d")
           end = datetime.strptime(end_date, "%Y-%m-%d")
           with SessionLocal() as session:
               query = session.query(Prediction).filter(Prediction.timestamp >= start, Prediction.timestamp <= end)
               if source != "all":
                   query = query.filter(Prediction.source == source)
               results = [
                   {"features": pred.features, "prediction": pred.prediction, "source": pred.source, "timestamp": pred.timestamp}
                   for pred in query.all()
               ]
           return results
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))