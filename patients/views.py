# from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import HealthRecordForm
from .models import HealthRecord
from django.shortcuts import get_object_or_404
from ml.utils.predict import predict_diabetes

# Create your views here.
@login_required
def new_assessment(request):
    form = HealthRecordForm()
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
    if form.is_valid():
        assessment = form.save(commit=False)
        assessment.user = request.user
        # Calculate BMI
        height_m = assessment.height / 100
        assessment.bmi = round(assessment.weight/(height_m ** 2), 2)
        #convert blood pressure "120/80" -> 120
        systolic_bp = int(assessment.blood_pressure.split('/')[0])
        #prepare ml input data
        # Estimated values for unavailable clinical features
        skin_thickness = 20      # median value from Pima dataset
        insulin = 125            # median value from Pima dataset


        # Convert family history into diabetes pedigree estimate
        if assessment.family_history == "Yes":
            diabetes_pedigree = 0.8
        else:
            diabetes_pedigree = 0.3

        # Pima dataset contains clinical features not usually known by users.
        # Missing features are estimated using dataset median values
        # to maintain compatibility with the trained model.


        patient_data = [
            assessment.pregnancies,
            assessment.glucose,
            systolic_bp,
            skin_thickness,
            insulin,
            assessment.bmi,
            diabetes_pedigree,
            assessment.age
        ]
        #ai prediction
        result = predict_diabetes(patient_data)
        #save ai result
        assessment.diabetes_prediction = result["result"]
        assessment.diabetes_confidence = result["confidence"]
        assessment.save()
        return redirect("/dashboard/")
    return render(request, 'patients/new_assessment.html', {'form': form})

@login_required
def history(request):
    records = HealthRecord.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'patients/history.html', {'records': records})   

@login_required
def history_detail(request, id):

    record = get_object_or_404(
        HealthRecord,
        id=id,
        user=request.user
    )

    context = {
        "record": record
    }

    return render(
        request,
        "patients/history_detail.html",
        context
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
        return redirect("patients:history")

    context = {
        "record": record
    }

    return render(
        request,
        "patients/delete_assessment.html",
        context
    )