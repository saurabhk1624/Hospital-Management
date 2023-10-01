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
    path('logouut/',views.logouut,name="logouut"),
    path('department/',views.department,name="department"),
    path('doctor/',views.doctor,name="doctor"),
    path('schedule/',views.schedule,name="schedule"),
    path('prescription/',views.prescription,name="prescription"),
    path('prescriptionpdf/',views.prescriptionpdf,name="prescriptionpdf"),
    path('reception/',views.reception,name="reception"),
    path('doctorlist/',views.doctorlist,name="doctorlist"),
    path('leftpanel/',views.leftpanel,name="leftpanel"),
    path('panelrouting/',views.panelrouting,name="panelrouting"),
    path('prescriptiondata/',views.prescriptiondata,name="prescriptiondata"),
    path('Payment/',views.Payment,name="Payment"),
    path('payapproval/',views.payapproval,name="payapproval"),
    path('paymentpdf/',views.paymentpdf,name="paymentpdf"),
    path('billdash/',views.billdash,name="billdash"),
    path('appointpayment/',views.appointpayment,name="appointpayment"),
    path('docapproval/',views.docapproval,name="docapproval"),
    path('recepreject/',views.recepreject,name="recepreject"),
    path('docreject/',views.docreject,name="docreject"),
    path('updateappoint/',views.updateappoint,name="updateappoint"),
    path('chart/',views.chart,name="chart"),
    path('luckydraw/',views.luckydraw,name="luckydraw"),
    path('previousappointment/',views.previousappointment,name="previousappointment"),
    

]