from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patients.models import HealthRecord


@login_required
def dashboard(request):

    records = HealthRecord.objects.filter(
        user=request.user
    ).order_by("-created_at")

    latest_record = records.first()

    context = {
        "records": records,
        "latest": latest_record,
        "total": records.count(),
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


@login_required
def ai_assistant(request):

    latest_record = HealthRecord.objects.filter(
        user=request.user
    ).order_by("-created_at").first()


    if not latest_record:

        return render(
            request,
            "dashboard/ai_assistant.html",
            {
                "record": None
            }
        )


    risk_factors = []
    analysis = []
    recommendations = []


    # -----------------------------
    # Glucose
    # -----------------------------

    if latest_record.glucose >= 140:

        risk_factors.append(
            "🔴 High Blood Glucose"
        )

        analysis.append(
            "Your blood glucose level is above the normal range, which is one of the strongest indicators of diabetes risk."
        )

        recommendations.append(
            "Reduce sugary foods and drinks and consult a healthcare provider for further evaluation."
        )

    else:

        analysis.append(
            "Your blood glucose level is within the normal range."
        )



    # -----------------------------
    # BMI
    # -----------------------------

    if latest_record.bmi >= 30:

        risk_factors.append(
            "🟡 High BMI"
        )

        analysis.append(
            "Your BMI indicates obesity, which may increase diabetes risk."
        )

        recommendations.append(
            "Exercise regularly and maintain a healthy diet."
        )


    elif latest_record.bmi >= 25:

        risk_factors.append(
            "🟡 Overweight"
        )

        analysis.append(
            "Your BMI is above the healthy range."
        )

        recommendations.append(
            "Try maintaining a healthy weight."
        )


    else:

        analysis.append(
            "Your BMI is within the healthy range."
        )



    # -----------------------------
    # Blood Pressure
    # -----------------------------

    try:

        systolic_bp = int(
            latest_record.blood_pressure.split("/")[0]
        )

    except:

        systolic_bp = 120



    if systolic_bp >= 130:

        risk_factors.append(
            "🟠 High Blood Pressure"
        )

        analysis.append(
            "Your blood pressure is elevated, which may increase overall health risks."
        )

        recommendations.append(
            "Monitor your blood pressure and consult a healthcare provider."
        )


    else:

        analysis.append(
            "Your blood pressure is within the normal range."
        )



    # -----------------------------
    # Family History
    # -----------------------------

    if latest_record.family_history == "Yes":

        risk_factors.append(
            "🧬 Family History"
        )

        analysis.append(
            "Having a family history of diabetes increases your risk."
        )

        recommendations.append(
            "Routine diabetes screening is recommended."
        )



    # -----------------------------
    # Smoking
    # -----------------------------

    if latest_record.smoking == "Yes":

        risk_factors.append(
            "🚬 Smoking"
        )

        analysis.append(
            "Smoking increases the risk of diabetes and other chronic diseases."
        )

        recommendations.append(
            "Consider quitting smoking."
        )



    # -----------------------------
    # Exercise
    # -----------------------------

    if latest_record.exercise == "Low":

        risk_factors.append(
            "🏃 Low Physical Activity"
        )

        analysis.append(
            "Low physical activity can contribute to diabetes and cardiovascular disease."
        )

        recommendations.append(
            "Aim for at least 30 minutes of exercise on most days."
        )



    # -----------------------------
    # Sleep
    # -----------------------------

    if latest_record.sleep < 7:

        analysis.append(
            "Sleeping less than 7 hours may affect blood sugar regulation."
        )

        recommendations.append(
            "Aim for 7–9 hours of quality sleep every night."
        )



    # -----------------------------
    # AI Risk Level
    # Uses diabetic probability
    # NOT confidence
    # -----------------------------

    diabetic_probability = (
        latest_record.diabetic_probability
    )


    if diabetic_probability >= 80:

        risk_level = "🔴 High"


    elif diabetic_probability >= 50:

        risk_level = "🟡 Moderate"


    else:

        risk_level = "🟢 Low"



    # -----------------------------
    # AI Summary
    # -----------------------------

    clean_risk = (
        risk_level
        .replace("🔴", "")
        .replace("🟡", "")
        .replace("🟢", "")
        .strip()
    )


    summary = (

        f"I analyzed your latest health assessment and identified "
        f"{len(risk_factors)} major risk factor(s). "

        f"Your AI prediction is "
        f"{latest_record.diabetes_prediction}. "

        f"Based on your health information, your diabetes risk level is "
        f"{clean_risk}. "

        f"The estimated diabetes probability is "
        f"{latest_record.diabetic_probability}%."

    )



    # -----------------------------
    # Disclaimer
    # -----------------------------

    disclaimer = (

        "This analysis is generated by HealthRisk AI and is intended "
        "for educational purposes only. It should not replace professional "
        "medical advice or diagnosis."

    )



    # -----------------------------
    # Positive Message
    # -----------------------------

    if len(risk_factors) == 0:

        analysis.append(
            "Great job! No major diabetes risk factors were identified in your assessment."
        )



    context = {

        "record": latest_record,

        "risk_level": risk_level,

        "risk_factors": risk_factors,

        "analysis": analysis,

        "recommendations": recommendations,

        "summary": summary,

        "disclaimer": disclaimer,

    }



    return render(
        request,
        "dashboard/ai_assistant.html",
        context
    )