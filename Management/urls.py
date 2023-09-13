from Management import views
from django.urls import path



urlpatterns = [
    path('patientregister/',views.patientregister,name="patientregister"),
    path('patientlogin/',views.patientlogin,name="patientlogin"),
    path('staffregister/',views.staffregister,name="staffregister"),
    path('stafflogin/',views.stafflogin,name="stafflogin"),
    path('patient/',views.patient,name="patient"),
    path('appointment/',views.appointment,name="appointment"),
    path('showpatient/',views.showpatient,name="showpatient"),
    path('showdoctor/',views.showdoctor,name="showdoctor"),
    path('doctorpatients/',views.doctorpatients,name="doctorpatients"),
    path('doctordash/',views.doctordash,name="doctordash"),
    path('individualpatient/',views.individualpatient,name="individualpatient"),
]
