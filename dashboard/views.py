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