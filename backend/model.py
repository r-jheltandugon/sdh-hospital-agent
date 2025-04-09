def predict_disease(symptoms: str, vitals: dict) -> str:
    # Simple rule-based prediction for demonstration
    if "fever" in symptoms and "cough" in symptoms:
        return "Possible Flu or COVID-19"
    elif "headache" in symptoms and "nausea" in symptoms:
        return "Possible Migraine"
    else:
        return "Unknown Disease"
