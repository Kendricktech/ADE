from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserRegistrationForm, CustomUserUpdateForm, ProfileForm  # Import custom forms
from django.conf import settings
User =settings.AUTH_USER_MODEL
import logging
logger = logging.getLogger(__name__)
class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('index')


    from django.contrib.auth import login as auth_login
    import logging

    

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = form.cleaned_data.get("is_agent", False)
        user.is_worker = form.cleaned_data.get("is_worker", False)
        
        logger.debug(f"User created: {user.username}, is_agent: {user.is_agent}, is_worker: {user.is_worker}")
        
        # Check if user is trying to be both agent and worker
        if user.is_agent and user.is_worker:
            form.add_error(None, "You can only choose one role: either Agent or Worker.")
            return self.form_invalid(form)
        
        # Handle agent-specific logic
        if user.is_agent:
            user.save()
            auth_login(self.request, user)
            logger.debug(f"User {user.username} logged in as an agent.")
            return redirect('services:create_agent')

        # Handle worker-specific logic
        if user.is_worker:
            user.save()
            auth_login(self.request, user)
            logger.debug(f"User {user.username} logged in as a worker.")
            return redirect('services:create_worker')

        # If neither, just save and log in the user
        user.save()
        auth_login(self.request, user)
        logger.debug(f"User {user.username} logged in with no role.")
        return super().form_valid(form)


class LoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy('index')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class UpdateUserView(UpdateView):
    model = User  # Adjust based on your user model
    form_class = CustomUserUpdateForm
    template_name = 'accounts/update.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user  # Only allow the logged-in user to update their profile


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
        return render(request, 'accounts/profile.html', {'form': form})
