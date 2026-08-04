from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import HealthRecordForm
from .models import HealthRecord

from ml.utils.predict import predict_diabetes


@login_required
def new_assessment(request):

    form = HealthRecordForm()

    if request.method == "POST":

        form = HealthRecordForm(request.POST)

        if form.is_valid():

            assessment = form.save(commit=False)

            assessment.user = request.user


            # -----------------------------
            # Calculate BMI
            # -----------------------------
            height_m = assessment.height / 100

            assessment.bmi = round(
                assessment.weight / (height_m ** 2),
                2
            )


            # -----------------------------
            # Convert Blood Pressure
            # Example: 120/80 -> 120
            # -----------------------------
            try:

                systolic_bp = int(
                    assessment.blood_pressure.split("/")[0]
                )

            except:

                systolic_bp = 120
            # -----------------------------
            # Estimated clinical values
            # From Pima Diabetes Dataset
            # -----------------------------
            skin_thickness = 20

            insulin = 125



            # -----------------------------
            # Family History Conversion
            # Diabetes Pedigree Estimate
            # -----------------------------
            if assessment.family_history == "Yes":

                diabetes_pedigree = 0.8

            else:

                diabetes_pedigree = 0.3



            # -----------------------------
            # Pregnancy Handling
            # Male users do not have pregnancy data.
            # ML model requires this value,
            # so male users get 0.
            # -----------------------------
            if assessment.gender == "Male":

                pregnancies = 0

            else:

                pregnancies = assessment.pregnancies or 0
            # -----------------------------
            # Prepare ML Input
            # Order must match model:
            #
            # Pregnancies
            # Glucose
            # BloodPressure
            # SkinThickness
            # Insulin
            # BMI
            # DiabetesPedigreeFunction
            # Age
            # -----------------------------

            patient_data = [

                pregnancies,

                assessment.glucose,

                systolic_bp,

                skin_thickness,

                insulin,

                assessment.bmi,

                diabetes_pedigree,

                assessment.age,

            ]
            # -----------------------------
            # AI Prediction
            # -----------------------------
            result = predict_diabetes(patient_data)



            # -----------------------------
            # Save AI Results
            # -----------------------------

            assessment.diabetes_prediction = (
                result["result"]
            )


            assessment.diabetes_confidence = (
                result["confidence"]
            )


            assessment.diabetic_probability = (
                result["diabetic_probability"]
            )


            assessment.non_diabetic_probability = (
                result["non_diabetic_probability"]
            )



            # Save record
            assessment.save()



            return redirect(
                "patients:processing"
            )



    return render(
        request,
        "patients/new_assessment.html",
        {
            "form": form
        }
    )



@login_required
def history(request):

    records = HealthRecord.objects.filter(
        user=request.user
    ).order_by("-created_at")


    return render(
        request,
        "patients/history.html",
        {
            "records": records
        }
    )



@login_required
def history_detail(request, id):

    record = get_object_or_404(
        HealthRecord,
        id=id,
        user=request.user
    )


    return render(
        request,
        "patients/history_detail.html",
        {
            "record": record
        }
    )



@login_required
def delete_assessment(request, id):

    record = get_object_or_404(
        HealthRecord,
        id=id,
        user=request.user
    )


    if request.method == "POST":

        record.delete()

        return redirect(
            "patients:history"
        )


    return render(
        request,
        "patients/delete_assessment.html",
        {
            "record": record
        }
    )



@login_required
def assessment_result(request, id):

    record = get_object_or_404(
        HealthRecord,
        id=id,
        user=request.user
    )


    return render(
        request,
        "patients/assessment_result.html",
        {"record": record}
    )



@login_required
def processing(request):

    return render(
        request,"patients/processing.html",{"redirect_url": reverse("dashboard:ai_assistant")}
    )