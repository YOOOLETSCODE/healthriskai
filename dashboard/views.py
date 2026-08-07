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



    # ---------------------------------
    # Blood Glucose
    # ---------------------------------

    if latest_record.blood_glucose_level >= 140:


        risk_factors.append(
            "🔴 High Blood Glucose"
        )


        analysis.append(
            "Your blood glucose level is above the normal range, which is one of the strongest indicators of diabetes risk."
        )


        recommendations.append(
            "Monitor glucose levels and reduce excessive sugar intake."
        )


    else:


        analysis.append(
            "Your blood glucose level is within the expected range."
        )





    # ---------------------------------
    # HbA1c
    # ---------------------------------

    if latest_record.hbA1c_level >= 6.5:


        risk_factors.append(
            "🔴 High HbA1c Level"
        )


        analysis.append(
            "Your HbA1c level indicates increased average blood sugar over recent months."
        )


        recommendations.append(
            "Consult a healthcare provider for diabetes evaluation."
        )



    elif latest_record.hbA1c_level >= 5.7:


        risk_factors.append(
            "🟡 Elevated HbA1c"
        )


        analysis.append(
            "Your HbA1c level is above the normal range."
        )


        recommendations.append(
            "Maintain a balanced diet and regular activity."
        )





    # ---------------------------------
    # BMI
    # ---------------------------------

    if latest_record.bmi >= 30:


        risk_factors.append(
            "🟡 High BMI"
        )


        analysis.append(
            "Your BMI indicates obesity, which may increase diabetes risk."
        )


        recommendations.append(
            "Focus on healthy weight management through diet and exercise."
        )



    elif latest_record.bmi >= 25:


        risk_factors.append(
            "🟡 Overweight"
        )


        analysis.append(
            "Your BMI is above the healthy range."
        )


        recommendations.append(
            "Maintaining a healthy weight can reduce diabetes risk."
        )


    else:


        analysis.append(
            "Your BMI is within the healthy range."
        )





    # ---------------------------------
    # Hypertension
    # ---------------------------------

    if latest_record.hypertension == 1:


        risk_factors.append(
            "🟠 Hypertension"
        )


        analysis.append(
            "High blood pressure can increase the risk of diabetes-related complications."
        )


        recommendations.append(
            "Monitor blood pressure regularly."
        )


    else:


        analysis.append(
            "No hypertension risk was reported."
        )





    # ---------------------------------
    # Heart Disease
    # ---------------------------------

    if latest_record.heart_disease == 1:


        risk_factors.append(
            "❤️ Heart Disease History"
        )


        analysis.append(
            "A history of heart disease is associated with higher metabolic risk."
        )


        recommendations.append(
            "Regular medical checkups are recommended."
        )





    # ---------------------------------
    # Smoking
    # ---------------------------------

    if latest_record.smoking_history in [
        "current",
        "ever",
        "former"
    ]:


        risk_factors.append(
            "🚬 Smoking History"
        )


        analysis.append(
            "Smoking history can increase diabetes and cardiovascular risk."
        )


        recommendations.append(
            "Avoid smoking and consider cessation support."
        )





    # ---------------------------------
    # AI Probability Risk
    # ---------------------------------

    diabetic_probability = (
        latest_record.diabetic_probability
    )



    if diabetic_probability >= 80:

        risk_level = "🔴 High"



    elif diabetic_probability >= 50:

        risk_level = "🟡 Moderate"



    else:

        risk_level = "🟢 Low"





    clean_risk = (
        risk_level
        .replace("🔴", "")
        .replace("🟡", "")
        .replace("🟢", "")
        .strip()
    )





    summary = (

        f"I analyzed your latest health assessment and identified "
        f"{len(risk_factors)} risk factor(s). "

        f"Your AI prediction is "
        f"{latest_record.diabetes_prediction}. "

        f"Your estimated diabetes risk level is "
        f"{clean_risk}. "

        f"The estimated diabetes probability is "
        f"{latest_record.diabetic_probability}%."

    )





    disclaimer = (

        "This analysis is generated by HealthRisk AI and is intended "
        "for educational purposes only. It does not replace professional "
        "medical advice or diagnosis."

    )





    if len(risk_factors) == 0:


        analysis.append(
            "Great job! No major diabetes risk factors were identified."
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