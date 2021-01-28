from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PatientListView, PatientCreateView, PatientList, PatientDetail
from. import views

urlpatterns = [
    path('', PatientListView.as_view(), name="patient_list"),
    path('create/', PatientCreateView.as_view(), name="patient_create"),


    #api views
    path('get_api/', PatientList.as_view(), name="patient_list_api"),
    path('get_api/<int:pk>/', PatientDetail.as_view(), name="patient_detail")
]