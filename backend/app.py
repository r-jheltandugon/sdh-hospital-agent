from fastapi import FastAPI
from pydantic import BaseModel
from . import model  # This will hold the logic for predicting disease based on symptoms

app = FastAPI()

class PatientSymptoms(BaseModel):
    symptoms: str
    vitals: dict

@app.post("/predict-disease")
def predict_disease(patient: PatientSymptoms):
    # Call the AI model to predict the disease based on symptoms and vitals
    disease = model.predict_disease(patient.symptoms, patient.vitals)
    return {"predicted_disease": disease}
