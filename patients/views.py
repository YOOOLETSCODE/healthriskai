from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import HealthRecordForm
from .models import HealthRecord
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required
def new_assessment(request):
    form = HealthRecordForm()
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
    if form.is_valid():
        assessment = form.save(commit=False)
        assessment.user = request.user
        height_m = assessment.height / 100
        assessment.bmi = round(assessment.weight / (height_m ** 2),2)
        assessment.save()
        return redirect("/dashboard/")
    return render(request, 'patients/new_assessment.html', {'form': form})

@login_required
def history(request):
    records = HealthRecord.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'patients/history.html', {'records': records})
    context = {
        'records': records
    }
    return render(request, 'patients/history.html', context)    

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