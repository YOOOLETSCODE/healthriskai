from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.
def signup(request):
    user_detail = SignupForm()
    print(user_detail)
    if request.method == 'POST':
        user_detail = SignupForm(request.POST)
        print(user_detail)

        if user_detail.is_valid():
            user_detail.save()
            return redirect('/accounts/login/')
    return render(request,'registration/signup.html',{'form':user_detail})

def loginuser(request):
    user_detail = AuthenticationForm()
    if request.method == 'POST':
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        val = authenticate(request, username=uname, password=upass)
        if val != None:
            login(request, val)
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'registration/login.html', {'form': user_detail})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('/accounts/login/')