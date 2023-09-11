from Management import views
from django.urls import path



urlpatterns = [
    path('patientregister/',views.patientregister,name="patientregister"),
    path('patientlogin/',views.patientlogin,name="patientlogin"),
    path('staffregister/',views.staffregister,name="staffregister"),
    path('stafflogin/',views.stafflogin,name="stafflogin"),
    
]
