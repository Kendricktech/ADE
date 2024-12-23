from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    is_agent = forms.BooleanField(required=False, label="Are you an agent?")

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "is_agent")


class CustomUserUpdateForm(UserChangeForm):  # Use UserChangeForm for updates
    class Meta:
        model = CustomUser
        fields = ("username", "is_agent")  # Include fields you want to update


# accounts/forms.py
from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'is_agent', 'is_worker']
        widgets = {
            'is_agent': forms.CheckboxInput(),
            'is_worker': forms.CheckboxInput(),
        }
