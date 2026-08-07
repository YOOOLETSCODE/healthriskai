from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import HealthRecordForm
from .models import HealthRecord
from ml.utils.predict import predict_diabetes

@login_required
def new_assessment(request):


    if request.method == "POST":


        form = HealthRecordForm(request.POST)



        if form.is_valid():


            assessment = form.save(
                commit=False
            )


            assessment.user = request.user



            patient_data = {



                "age":
                    assessment.age,



                "race:AfricanAmerican":
                    1 if assessment.race=="AfricanAmerican" else 0,


                "race:Asian":
                    1 if assessment.race=="Asian" else 0,


                "race:Caucasian":
                    1 if assessment.race=="Caucasian" else 0,


                "race:Hispanic":
                    1 if assessment.race=="Hispanic" else 0,


                "race:Other":
                    1 if assessment.race=="Other" else 0,



                "hypertension":
                    assessment.hypertension,



                "heart_disease":
                    assessment.heart_disease,



                "bmi":
                    assessment.bmi,



                "hbA1c_level":
                    assessment.hbA1c_level,



                "blood_glucose_level":
                    assessment.blood_glucose_level,



                "gender_Female":
                    1 if assessment.gender=="Female" else 0,


                "gender_Male":
                    1 if assessment.gender=="Male" else 0,



                "smoking_history_No Info":
                    1 if assessment.smoking_history=="No Info" else 0,


                "smoking_history_current":
                    1 if assessment.smoking_history=="current" else 0,


                "smoking_history_ever":
                    1 if assessment.smoking_history=="ever" else 0,


                "smoking_history_former":
                    1 if assessment.smoking_history=="former" else 0,


                "smoking_history_never":
                    1 if assessment.smoking_history=="never" else 0,


                "smoking_history_not current":
                    1 if assessment.smoking_history=="not current" else 0,

            }



            result = predict_diabetes(
                patient_data
            )



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



            assessment.save()



            return redirect(
                "patients:processing"
            )



    else:

        form = HealthRecordForm()



    return render(
        request,
        "patients/new_assessment.html",
        {
            "form":form
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
        {
            "record": record
        }
    )



@login_required
def processing(request):

    return render(
        request,
        "patients/processing.html",
        {
            "redirect_url": reverse(
                "dashboard:ai_assistant"
            )
        }
    )