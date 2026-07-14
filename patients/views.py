from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import HealthRecordForm

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