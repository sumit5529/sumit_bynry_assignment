

from .models import ServiceRequest
from django import forms
class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'  
