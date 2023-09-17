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
    path('recepapproval/',views.recepapproval,name="recepapproval"),
    path('docappoint/',views.docappoint,name="docappoint"),
    path('recepappoint/',views.recepappoint,name="recepappoint"),
    path('patientappoint/',views.patientappoint,name="patientappoint"),
    path('render_app/',views.render_app,name="render_app"),
    path('logout/',views.logout,name="logout"),
    # path('getpdf/',views.getpdf,name="getpdf"),
    path('department/',views.department,name="department"),
    path('doctor/',views.doctor,name="doctor"),





]