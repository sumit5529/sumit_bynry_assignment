# Ensure fields are not excluded in the Meta class of a ModelForm if used.

from .models import ServiceRequest
from django import forms
class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'  # Ensure all fields are included or specific fields needed
