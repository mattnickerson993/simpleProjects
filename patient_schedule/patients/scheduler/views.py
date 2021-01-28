from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from .models import Patient
from .forms import NewPatientForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class PatientListView(ListView):

    model = Patient
    context_object_name = 'patients'
    extra_context = {'patientForm': NewPatientForm }


class PatientCreateView(CreateView):
    model = Patient
    fields = ['name', 'appointment_date', 'appointment_time']
    success_url = "/schedule/"

    def form_valid(self, form):
        form.instance.therapist = self.request.user
        return super().form_valid(form)

# @api_view(['GET', 'POST'])
# def patient_list_api(request):

#     if request.method == 'GET':
#         patients = Patient.objects.all()
#         serializer = PatientSerializer(patients, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = PatientSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PatientList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(therapist=self.request.user)


class PatientDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        patient = self.get_object(pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)