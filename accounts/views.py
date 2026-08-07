from django.shortcuts import render, redirect
from django.http import HttpResponse

from patients.models import HealthRecord
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def signup(request):
    user_detail = SignupForm()
    print(user_detail)
    if request.method == 'POST':
        user_detail = SignupForm(request.POST)
        print(user_detail)

        if user_detail.is_valid():
            user_detail.save()
            return redirect('accounts:login')
    return render(request,'registration/signup.html',{'form':user_detail})

def loginuser(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            user = None

        if user is not None:

            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password,
            )

            if authenticated_user:

                login(request, authenticated_user)

                return redirect("/dashboard/")

        messages.error(
            request,
            "Invalid email or password."
        )

    return render(
        request,
        "registration/login.html"
    )

@login_required
def profile(request):

    records = HealthRecord.objects.filter(
        user=request.user
    ).order_by('-created_at')

    latest = records.first()

    context = {
        "latest": latest,
        "total": records.count()
    }

    return render(
        request,
        "accounts/profile.html",
        context
    )


@login_required
def logoutuser(request):

    logout(request)

    return redirect("accounts:login")

