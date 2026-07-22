from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patients.models import HealthRecord


@login_required
def dashboard(request):

    records = HealthRecord.objects.filter(user=request.user).order_by("-created_at")

    latest_record = records.first()

    context = {
        "records": records,
        "latest": latest_record,
        "total": records.count(),
    }

    return render(request, "dashboard/dashboard.html", context)

@login_required
def ai_assistant(request):
    latest_record = HealthRecord.objects.filter(
        user=request.user).order_by('-created_at').first()

    return render(request,"dashboard/ai_assistant.html",{"record": latest_record})