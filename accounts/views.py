from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
def signup(request):
    user_detail = SignupForm()
    if request.method == 'POST':
        user_detail = SignupForm(request.POST)

        if user_detail.is_valid():
            form = user_detail.save()
            login(request, form)
            return redirect('accounts:profile')
        else:
            form = SignupForm()
    return render(request,'registration/signup.html',{'form':user_detail})