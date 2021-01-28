from django.forms import ModelForm
from .models import Patient

class NewPatientForm(ModelForm):
    
    class Meta:
        model = Patient
        fields = ['name', 'appointment_date', 'appointment_time']