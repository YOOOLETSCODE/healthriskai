from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from patients.models import HealthRecord
from .forms import SignupForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Intercept save to properly hash raw password
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        # Safely capture either email or username form inputs
        email_or_username = request.POST.get('email') or request.POST.get('username')
        password = request.POST.get('password')

        # Find user by case-insensitive email lookup
        try:
            user_obj = User.objects.get(email__iexact=email_or_username)
        except User.DoesNotExist:
            # Fallback to checking username if email wasn't found
            user_obj = User.objects.filter(username__iexact=email_or_username).first()

        if user_obj is not None:
            # Authenticate using the matched user's username
            authenticated_user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                
                # Check for 'next' parameter in redirect URL or default to dashboard
                next_url = request.GET.get('next') or request.POST.get('next')
                return redirect(next_url if next_url else '/dashboard/')

        messages.error(request, "Invalid email/username or password.")

    return render(request, 'registration/login.html')


@login_required
def profile(request):
    records = HealthRecord.objects.filter(user=request.user).order_by('-created_at')
    latest = records.first()

    context = {
        'latest': latest,
        'total': records.count()
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def logoutuser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')