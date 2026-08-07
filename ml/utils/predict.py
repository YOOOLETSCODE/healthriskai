import os
import joblib
import pandas as pd


# ml/utils/predict.py
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


MODEL_PATH = os.path.join(
    BASE_DIR,
    "trained_models",
    "diabetes_xgb_model.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR,
    "trained_models",
    "feature_names.pkl"
)


# Load model and feature order
model = joblib.load(MODEL_PATH)
FEATURES = joblib.load(FEATURE_PATH)



def predict_diabetes(data):
    """
    Predict diabetes risk using XGBoost model.

    Returns:
    - prediction
    - result
    - confidence
    - diabetic_probability
    - non_diabetic_probability
    """

    # Create dataframe using training feature order
    patient = pd.DataFrame([data])
    patient = patient[FEATURES]


    # Prediction
    prediction = int(
        model.predict(patient)[0]
    )


    # Probability
    probabilities = model.predict_proba(patient)[0]


    non_diabetic_probability = round(
        float(probabilities[0] * 100),
        2
    )

    diabetic_probability = round(
        float(probabilities[1] * 100),
        2
    )


    if prediction == 1:
        result = "High Diabetes Risk"
        confidence = diabetic_probability

    else:
        result = "Low Diabetes Risk"
        confidence = non_diabetic_probability


    return {
        "prediction": prediction,
        "result": result,
        "confidence": confidence,
        "diabetic_probability": diabetic_probability,
        "non_diabetic_probability": non_diabetic_probability,
    }