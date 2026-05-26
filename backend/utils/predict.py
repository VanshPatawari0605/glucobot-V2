import numpy as np
import joblib
import os


def load_model():
    try:
        base = os.path.dirname(os.path.dirname(__file__))
        m = joblib.load(os.path.join(base, "model", "diabetes_model.pkl"))
        s = joblib.load(os.path.join(base, "model", "scaler.pkl"))
        return m, s
    except Exception as e:
        print(f"[ERROR] Could not load model: {e}")
        return None, None


def run_prediction(model, scaler, inputs: dict) -> dict:
    preg    = inputs["pregnancies"]
    glucose = inputs["glucose"]
    bp      = inputs["blood_pressure"]
    skin    = inputs["skin_thickness"]
    insulin = inputs["insulin"]
    bmi     = inputs["bmi"]
    dpf     = inputs["dpf"]
    age     = inputs["age"]

    # Engineered features — must match train.py exactly
    bmi_age            = bmi * age
    glucose_insulin    = glucose * insulin
    glucose_bmi        = glucose * bmi
    glucose_age        = glucose / (age + 1)
    insulin_resistance = insulin / (glucose + 1)
    bmi_category       = 1 if bmi >= 30 else 0

    data = np.array([[
        preg, glucose, bp, skin, insulin, bmi, dpf, age,
        bmi_age, glucose_insulin, glucose_bmi,
        glucose_age, insulin_resistance, bmi_category
    ]])

    scaled = scaler.transform(data)
    prob   = float(model.predict_proba(scaled)[0][1])

    if prob < 0.35:
        label = "LOW RISK"
    elif prob < 0.65:
        label = "MODERATE RISK"
    else:
        label = "HIGH RISK"

    return {
        "probability": round(prob, 4),
        "percentage":  round(prob * 100, 1),
        "label":       label,
    }