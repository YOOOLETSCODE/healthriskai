import os
import joblib
import pandas as pd

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Model path
MODEL_PATH = os.path.join(
    BASE_DIR,
    "trained_models",
    "diabetes_model.pkl"
)

# Features expected by the model
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

# Load trained model
model = joblib.load(MODEL_PATH)


def predict_diabetes(data):
    """
    Predict diabetes and return:
    - prediction (0 or 1)
    - result (Diabetic / Non-Diabetic)
    - confidence (confidence of the predicted class)
    - diabetic_probability
    - non_diabetic_probability
    """

    # Convert input into DataFrame
    patient = pd.DataFrame([data], columns=FEATURES)

    # Predict class
    prediction = int(model.predict(patient)[0])

    # Get probabilities
    probabilities = model.predict_proba(patient)[0]

    # Assuming model.classes_ == [0, 1]
    non_diabetic_probability = round(float(probabilities[0] * 100), 2)
    diabetic_probability = round(float(probabilities[1] * 100), 2)

    # Human-readable result
    if prediction == 1:
        result = "Diabetic"
        confidence = diabetic_probability
    else:
        result = "Non-Diabetic"
        confidence = non_diabetic_probability

    return {
        "prediction": prediction,
        "result": result,
        "confidence": confidence,
        "diabetic_probability": diabetic_probability,
        "non_diabetic_probability": non_diabetic_probability,
    }