from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm, CustomUserUpdateForm  # Import the custom forms

def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create a new user instance
            user.is_agent = form.cleaned_data["is_agent"]  # Set is_agent based on form input
            user.save()  # Save the user
            auth_login(request, user)  # Log the user in after registration
            return redirect("index")  # Redirect to the home page
    else:
        form = CustomUserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

def login(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirect if user is already logged in

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Get next parameter or default to index
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def custom_logout(request):
    auth_logout(request)  # Use auth_logout to log out the user
    return redirect('accounts:login')  # Redirect to the login page

@login_required  # Ensure only logged-in users can access this
def update_user(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect after successful update
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'accounts/update.html', {'form': form})


# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = ProfileForm(instance=user)
    
    return render(request, 'accounts/profile.html', {'form': form})
