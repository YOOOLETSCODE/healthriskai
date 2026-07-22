import os
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "trained_models",
    "diabetes_model.pkl"
)

FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]



model = joblib.load(MODEL_PATH)


def predict_diabetes(data):
    patient = pd.DataFrame([data], columns=FEATURES)
    prediction = int(model.predict(patient)[0])

    probabilities = model.predict_proba(patient)[0]

    confidence = float(round(max(probabilities) * 100, 2))

    result = "Diabetic" if prediction == 1 else "Non-Diabetic"

    return {
        "prediction": prediction,
        "result": result,
        "confidence": confidence,
    }