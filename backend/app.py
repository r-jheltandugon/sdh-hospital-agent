from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import Optional

app = FastAPI()

# Serve static files like HTML, CSS, JS from the "frontend" directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Define the conversation state
class ConversationState(BaseModel):
    symptoms: Optional[str] = None
    heart_rate: Optional[int] = None
    blood_pressure: Optional[str] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[int] = None
    step: int = 0  # Track which step in the conversation the user is at

# Simple rule-based model for disease prediction
def predict_disease(symptoms, vitals):
    if "headache" in symptoms.lower() and "dizziness" in symptoms.lower() and vitals['blood_pressure'] == "150/100":
        return "Hypertension"
    if "fever" in symptoms.lower() and "cough" in symptoms.lower():
        return "Flu"
    if "chest pain" in symptoms.lower() and vitals['heart_rate'] > 100:
        return "Heart Attack"
    return "Unknown Disease"

@app.post("/conversation")
async def conversation(state: ConversationState):
    # Begin the conversation or continue based on the state
    if state.step == 0:
        return {"message": "Please tell me your symptoms."}
    
    if state.step == 1 and state.symptoms:
        return {"message": "Got it! Now, what is your temperature (in °C)?"}
    
    if state.step == 2 and state.temperature:
        return {"message": "Thanks! What is your heart rate?"}
    
    if state.step == 3 and state.heart_rate:
        return {"message": "Got it! What is your blood pressure?"}
    
    if state.step == 4 and state.blood_pressure:
        return {"message": "Thanks! Finally, what's your respiratory rate?"}
    
    if state.step == 5 and state.respiratory_rate:
        # Now predict the disease based on gathered data
        vitals = {
            "heart_rate": state.heart_rate,
            "blood_pressure": state.blood_pressure,
            "temperature": state.temperature,
            "respiratory_rate": state.respiratory_rate
        }
        predicted_disease = predict_disease(state.symptoms, vitals)
        return {"message": f"Based on the symptoms and vitals provided, the predicted disease is: {predicted_disease}"}
    
    # Update conversation step
    state.step += 1
    return state

