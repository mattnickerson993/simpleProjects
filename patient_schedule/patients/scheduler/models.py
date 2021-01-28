from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    appointment_time= models.TimeField()
    appointment_date= models.DateField()
    name = models.CharField(max_length= 100)
    


    def __str__(self):
        return f"Appointment for {self.name} at {self.appointment_date} at {self.appointment_time}"