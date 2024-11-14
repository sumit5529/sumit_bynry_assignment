from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

# If you need a custom form, you can extend the existing AuthenticationForm:
# class CustomAuthenticationForm(AuthenticationForm):
#     # Add any custom validation or fields if necessary
#     pass