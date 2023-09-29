import json

import re

from django.http import   JsonResponse

from Hospital import settings

from .models import Leftpanel, Management, Patients, Prescription, Speciality, User,doctors,Appointments, payment,time

from django.contrib.auth import authenticate,login

from django.http import HttpResponse

from django.template.loader import render_to_string

from django_renderpdf.helpers import render_pdf

from django.core.mail import send_mail




# Registartion of patient

def patientregister(request):

    if request.method=='POST':

        data=json.loads(request.body)

        firstname=data['firstname']

        lastname=data['lastname']

        name=data['name']

        age=data['age']

        gender=data['gender']

        email=data['email']

        password=data['password']

        cpassword=data['confirmpassword']


        if not name or not email or not gender or not age or not password or not firstname or not lastname or not cpassword:
           
           return JsonResponse({'message':'All fields are required'},status=400)
     
        else:
         
          if not  re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email) :
          
           
           return JsonResponse({'message':'Not valid Email'},status=400)
         
          else:

           if User.objects.filter(username=name).exists():
           
            return JsonResponse({'message':'username already exist'},status=400)
          
           else: 
           
           
              if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,15}$",password) is None:
             
                return JsonResponse({'message':'Password denied: Password is not valid'},status=400)
           
              else:
              
                if cpassword==password:

                 if User.objects.filter(email=email).exists():
                 
                  return JsonResponse({'message':'email already exist'},status=400)
                 

                 else:
               
                  table= User.objects.create_user(name,email,password)

                  Id=User.objects.get(email=email)
               
                  manage=Management.objects.create(title='Patient')

                  manage.user.add(table)
 
                  Patients.objects.create(firstname=firstname,lastname=lastname,age=age,gender=gender,user_id=Id.id,username=name)

                  Id.first_name=firstname
               
                  Id.last_name=lastname

                  Id.save()

                  return JsonResponse({'message':'Registration Successful'},status=200)
                  
                else:

                 return JsonResponse({'message':'Confirm Password not same'},status=401)
                      
    else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
    

    
# doctor department

def department(request):

  if request.method=='GET':

    info=Speciality.objects.filter(status=False).values('id','department')

    dept=list(info)

    return JsonResponse(dept,safe=False)
  
  else :

    return JsonResponse({'message':'Method not allowed'},status=405)
  


#  login of patient       

def patientlogin(request):
  
  if request.method=='POST':
     
     data1=json.loads(request.body)

     username= data1['username']

     password =data1['password']

     if not username or not password:
      
       return JsonResponse({'message':'All fields are required'},status=400)
     
     else:
  
      user = authenticate(username=username, password=password)

      if user  is not None:
        
          login(request,user)
          
          return JsonResponse({'message':'Logged in'},status=200)
        
      else:
        
        if User.objects.filter(username=username).exists():
       
         return JsonResponse({'message':'password is  not same'},status=400)
       
        else:
         
         return JsonResponse({'message':'Username is wrong'},status=400)     
     
  else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
  


# Registartion of doctors

def staffregister(request):

  if request.method=='POST':

        data2=json.loads(request.body)

        firstname=data2['firstname']

        lastname=data2['lastname']

        name=data2['name']

        gender=data2['gender']

        email=data2['email']

        speciality=data2['department']

        password=data2['password']

        cpassword=data2['confirmpassword']

        special=Speciality.objects.get(id=speciality)

        if not name or not email or not gender or not speciality or not password or not firstname or not lastname or not cpassword:
           
           return JsonResponse({'message':'All fields are required'},status=400)
     
        else:
         
         if not  re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email) :
           
           return JsonResponse({'message':'Not valid Email'},status=400)
         
         else:

          if User.objects.filter(email=email).exists():
           
           return JsonResponse({'message':'Email already exist'},status=400)
          
          else: 
           
            if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,15}$",password) is None:
             
              return JsonResponse({'message':'Password denied: Password is not valid'},status=400)
           
            else:
              
              if cpassword==password:
               
                if User.objects.filter(username=name).exists():
       
                    return JsonResponse({'message':'usrname already exist'},status=400)
       
                else:
               
                  table= User.objects.create_user(name,email,password,is_superuser=True)

                  user=User.objects.get(email=email)

                  manage=Management.objects.create(title='Patient')

                  manage.user.add(table)

                  doctors.objects.create(firstname=firstname,lastname=lastname,gender=gender,special_id=speciality,user_id=user.id,username=name,speciality=special.department)
               
                  user.first_name=firstname

                  user.last_name=lastname

                  user.save()

                  return JsonResponse({'message':'Registration Successful'},status=200)
              
              else:

                return JsonResponse({'message':'Confirm Password not same'},status=401)
              
  else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
  

# logout

def logout(request):

  if request.method=='POST':

    if request.user.is_authenticated:
     
     logout(request)

     return JsonResponse({'message':'Logged out successfully'},status=200)
    
    else:

      return JsonResponse({'message':'user is not logged in'},status=401)
    
  else:

    return JsonResponse({'message':'Method not allowed'},status=400)
  



# login of staff 
 
    
def stafflogin(request):

   if request.method=='POST':

     data1=json.loads(request.body)

     username= data1['username']

     password =data1['password']

     if not username or not password:
      
      return JsonResponse({'message':'All fields are required'},status=400)
     
     else:

       user = authenticate(username=username, password=password)

       if user  is not None:
        
           login(request,user)
           
           id=request.user.id

           info=Management.objects.get(user=id)

           if info.title=='Doctor':

            return JsonResponse({'message':'Doctor'},status=200)
          
           elif info.title=='Receptionist':

            return JsonResponse({'message':'Stafflogin'},status=200)
          
           else:

            return JsonResponse({'message':'Not a staff'},status=200)

       else:
       
        if User.objects.filter(username=username).exists():
       
         return JsonResponse({'message':'password is  not same'},status=400)
       
        else:
         
         return JsonResponse({'message':'Username is wrong'},status=400)
     
   else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)



# details of patient on patient dashboard


def patient(request):

  if request.method=='GET':

   if request.user.is_authenticated:

    user=request.user.id

    patientinfo=Patients.objects.filter(user_id=user).values('username','firstname','lastname','age','gender')

    info=list(patientinfo)

    return JsonResponse(info,safe=False)
  
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
   
  else :

    return JsonResponse({'message':'Method not allowed'},status=405) 
  

# doctor detail for doc dashboard

def doctor(request):

  if request.method=='GET':

   if request.user.is_authenticated :

    user=request.user.id

    role=Management.objects.get(user=user)
 
    if role.title=='Doctor':
    
     patientinfo=doctors.objects.filter(user_id=user).values('username','firstname','lastname','gender')

     info=list(patientinfo)

     return JsonResponse(info,safe=False)
    
    else:

      return JsonResponse({'message':'Not a doctor'},status=403)
  
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
   
  else :

    return JsonResponse({'message':'Method not allowed'},status=405) 
  
# receptionist dashboard

def reception(request):

  if request.method=='GET':

   if request.user.is_authenticated :

    user=request.user.id

    role=Management.objects.get(user=user)
 
    if role.title=='Receptionist':  
      
      patientinfo=doctors.objects.filter(user_id=user).values('username','firstname','lastname','gender')

      info=list(patientinfo)

      return JsonResponse(info,safe=False) 
    
    else:

      return JsonResponse({'message':'Not a Staff'},status=403)
   
  
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
   
  else :

    return JsonResponse({'message':'Method not allowed'},status=405) 
  

# schedule time
def schedule(request):

  if request.method=='GET':

    info=time.objects.filter(status=False).values('id','time')

    data=list(info)

    return JsonResponse(data,safe=False)
  
  else :

    return JsonResponse({'message':'Method not allowed'},status=405)




# for Appointment


def appointment(request):

  if request.method=='POST':

   if request.user.is_authenticated: 

    data3=json.loads(request.body)

    problem=data3['problem']

    medical=data3['medical']

    Time=data3['time']

    doctor=data3['doctor']

    date=data3['date']

    data=time.objects.get(id=Time)

    user=request.user.id
    
    # doc=doctors.objects.get(id=doctor)

    info=Patients.objects.get(user=user)

    if not problem or not medical or not Time or not doctor or not date :

      return JsonResponse({'message':'All fields are required'},status=400)
    
    else:
      
      if Patients.objects.filter(user=user,exist=False).exists():
       
        Appointments.objects.create(firstname=info.firstname,doctor_id=doctor,lastname=info.lastname,age=info.age,problem=problem,gender=info.gender,registerdate=date,time=data.time,medical=medical,patient_id=info.id)
        
        info.doctor_id=doctor
        
        info.exist=True

        info.save()

        return JsonResponse({'message':'Appointment applied'},status=200)
      
      else:

        Appointments.objects.create(firstname=info.firstname,doctor_id=doctor,lastname=info.lastname,age=info.age,problem=problem,gender=info.gender,registerdate=date,time=data.time,new=True,medical=medical,patient_id=info.id)
        
        info.doctor_id=doctor

        info.save()

        return JsonResponse({'message':'Appointment applied'},status=200)
      
   else:
     
     return JsonResponse({'message':'Not a Staff'},status=400)    
      
  else :

    return JsonResponse({'message':'Method not allowed'},status=405)  
  


# All Patient record for reception dashboard


def showpatient(request):

  if request.method=='GET':

    info=Patients.objects.all().values('user_id','firstname','lastname','age','gender')

    patient=list(info)

    return JsonResponse(patient,safe=False)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)


# approved appointment on patient dashboard

def patientappoint(request):

  if request.method=='GET':

   if request.user.is_authenticated:

    user=request.user.id
    
    data=Patients.objects.get(user=user)

    info=Appointments.objects.filter(patient=data.id,docapproval=True,paystatus=False,recepapproval=True).values('id','firstname','lastname','age','gender')

    appointment=list(info)

    return JsonResponse(appointment,safe=False)

   else:
     
     return JsonResponse({'message':'User is not authenticated'},status=401)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)



#All doctor record for receiption dashboard


def showdoctor(request):

  if request.method=='GET':

   if request.user.is_authenticated:

    user=request.user.id  

    role=Management.objects.get(user=user)
 
    if role.title=='Receptionist':

      info=doctors.objects.filter(reception=False).values('firstname','lastname','gender','user','speciality')

      doctor=list(info)

      return JsonResponse(doctor,safe=False)
    
    else:

      return JsonResponse({'message':'Not a staff'},status=403)
   
   else:
     
     return JsonResponse({'message':'Not a Staff'},status=400) 
   
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# Patient under each doctor for reception  dashboard


def doctorpatients(request):

  if request.method=='GET':
    
   if request.user.is_authenticated: 

    user=request.user.id  

    role=Management.objects.get(user=user)
 
    if role.title=='Receptionist':

   
     doctorid=request.GET.get('id')

     info=Patients.objects.filter(doctor_id=doctorid).values('firstname','lastname','age','gender')

     patients=list(info)

     return JsonResponse(patients,safe=False)
    
    else:

      return JsonResponse({'message':'Not a staff'},status=403)
  
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
  
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# patient under each doctor for  Doctor dashboard


def doctordash(request):

  if request.method=='GET':

   if request.user.is_authenticated: 

    user=request.user.id  

    role=Management.objects.get(user=user)
 
    if role.title=='Doctor':
    
     data=doctors.objects.get(user=user)
   
     info=Patients.objects.filter(doctor=data.id).values('username','firstname','lastname','age','gender')

     patients=list(info)

     return JsonResponse(patients,safe=False)
    
    else:

      return JsonResponse({'message':'Not a doctor'},status=403)
   
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# individual patient record on doctordashboard for prescription


def individualpatient(request):

  if request.method=='GET':
   
   if request.user.is_authenticated:

    user=request.user.id  

    role=Management.objects.get(user=user)
 
    if role.title=='Doctor':

     patientid=request.GET.get('patientid')

     info=Patients.objects.filter(id=patientid).values('firstname','lastname','age','gender')
 
     patient=list(info)

     return JsonResponse(patient,safe=False)
    
    else:

      return JsonResponse({'message':'Not a doctor'},status=403)
   
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  

# approval of appointment from receptionist

def recepapproval(request):

  if request.method=='PUT':
   
   if  request.user.is_authenticated:

    user=request.user.id  

    role=Management.objects.get(user=user)
 
    if role.title=='Receptionist':

     data=json.loads(request.body)

     appointid=data['id']

     reason=data['reason']

     Appointments.objects.filter(id=appointid).update(receparroval=True,reason=reason)

     info=Appointments.objects.get(id=appointid)
        
     loads=Patients.objects.get(id=info.patient_id)
 
     email=User.objects.get(id=loads.user_id)
    
     Doc=doctors.objects.get(id=loads.doctor_id)

     data={
       'Appointmentno':info.id,
       'Firstname':info.firstname,
       'Lastname':info.lastname,
       'Age':info.age,
       'Problem':info.problem,
       'Gender':info.gender,
       'Doctor':Doc.firstname,
        'Time':info.registerdate
        
       }
     subject='Regarding Appointment Status'

     from_email=settings.EMAIL_HOST_USER

     to_list=[email.email,]
     
     m='Your Appointment has been approved'

     message=render_to_string('Management/email.html',context=data)


     send_mail(subject,message=m,from_email=from_email,recipient_list=to_list,html_message=message,fail_silently=False)

     return JsonResponse({'message':'Appointment approved'},status=200)
    
    else:

      return JsonResponse({'message':'Not a staff'},status=403)
   
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
  
  elif request.method=='DELETE':

   if request.user.is_authenticated:

    user=request.user.id

    role=Management.objects.get(user=user)
 
    if role.title=='Receptionist':  
 
     data1=json.loads(request.body)

     appointid=data1['id']

     reason=data1['reason']

     Appointments.objects.filter(id=appointid).update(reject=True,reason=reason)

     info=Appointments.objects.get(id=appointid)
      
    
     loads=Patients.objects.get(id=info.patient_id)

     email=User.objects.get(id=loads.user_id)
    

     Doc=doctors.objects.get(id=loads.doctor_id)


     data={
       'Appointmentno':info.id,
       'Firstname':info.firstname,
       'Lastname':info.lastname,
       'Age':info.age,
       'Problem':info.problem,
       'Gender':info.gender,
       'Doctor':Doc.firstname,
        'Time':info.registerdate,
        'reason':info.reason
       }
     subject='Regarding Appointment Status'

     from_email=settings.EMAIL_HOST_USER

     to_list=[email.email,]
     
     m='Your Appointment has been rejected'

     message=render_to_string('Management/Rejection.html',context=data)


     send_mail(subject,message=m,from_email=from_email,recipient_list=to_list,html_message=message,fail_silently=False)

     return JsonResponse({'message':'Appointment rejected'},status=200)
    
    else:

      return JsonResponse({'message':'Not a Staff'},status=403)
   
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)

# all appointment for reception dashboard


def recepappoint(request):

    if request.method=='GET':
      
     if request.user.is_authenticated:

       user=request.user.id

       role=Management.objects.get(user=user)
  
       if role.title=='Receptionist':  


        info=Appointments.objects.filter(reject=False,paystatus=False,docapproval=False,recepapproval=False).values('id','firstname','lastname','age','problem','gender')

        patient=list(info)

        return JsonResponse(patient,safe=False)
       
       else:
         
         return JsonResponse({'message':'Not a staff'},status=403)
     
     else:
     
      return JsonResponse({'message':'Not authenticated'},status=401)  
    
    else :

      return JsonResponse({'message':'Method not allowed'},status=405)
    

# all appointment for doctor dashboard


def docappoint(request):

  if request.method=='GET':

   if  request.user.is_authenticated:

    user=request.user.id

    #  user=request.user.id

    role=Management.objects.get(user=user)
 
    if role.title=='Doctor':  


     data=doctors.objects.get(user=user)

     info=Appointments.objects.filter(doctor=data.id,reject=False,docapproval=False,recepapproval=True).values('id','firstname','lastname','age','problem','gender')

     patient=list(info)

     return JsonResponse(patient,safe=False)
    
    else:

      return JsonResponse({'message':'Not a doctor'},status=403)
   
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
  
  else :

    return JsonResponse({'message':'Method not allowed'},status=405)
  

# pdf generation of appointment

def render_app(request):

    if request.method=='POST':
      
     db=json.loads(request.body)

     appointid=db['id']
     
     info=Appointments.objects.get(id=appointid)
      
     loads=Patients.objects.get(id=info.patient_id)

     Doc=doctors.objects.get(id=loads.doctor_id)

     data={
       'Appointmentno':info.id,
       'Firstname':info.firstname,
       'Lastname':info.lastname,
       'Age':info.age,
       'Problem':info.problem,
       'Gender':info.gender,
       'Doctor':Doc.firstname,
       'Date':info.registerdate

       }
    
     template='Management/base.html'
    
     response = HttpResponse(content_type="application/pdf")
    
     response["Content-Disposition"] = 'attachment; filename="Appointment.pdf"'
                     
     render_pdf(
            template=template,
            file_=response,
            context=data,
      )
    return response

# prescription by doctor

def  prescription(request):

  if request.method=='POST':
    
    if request.user.is_authenticated :

     user=request.user.id

     role=Management.objects.get(user=user)
 
     if role.title=='Doctor':  


      loads=json.loads(request.body)

      for i in loads:

        id=i['Id']

        medicine_name=i['name']

        dosage=i['dose']
        
        instruction=i['instructions']

        info=Appointments.objects.get(id=id)
       
        if not medicine_name or not dosage or not instruction:

          return JsonResponse({'message':'All fields are required'},status=400)
     
        else:
       
              Prescription.objects.create(medicine_name=medicine_name,instruction=instruction,dosage=dosage,appointment_id=id,patient_id=info.patient_id)

      return JsonResponse({'message':'Prescription added'},status=200)
     
     else:
       
       return JsonResponse({'message':'Not a doctor'},status=403)
     
    else :

      return JsonResponse({'message':'User is not authenticated'},status=401)
    
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)


#  prescription data on patient dashboard

def prescriptionpdf(request):

  if request.method=='GET':
   
   if request.user.is_authenticated:
     
     user=request.user.id

     id=Patients.objects.get(user=user)

     info=Prescription.objects.filter(patient=id.id).values('appointment','medicine_name','dosage','instruction')

     data=list(info)

     return  JsonResponse(data,safe=False)
   
   else:
     
     return JsonResponse({'message':'User is not authenticated'},status=401)
   
  else:

    return JsonResponse({'message':'Method not allowed'},status=405) 

     

# dependent dropdown doctor list

def doctorlist(request):
  
  if request.method=='GET':
    
     if request.user.is_authenticated:
    
      id=request.GET.get('id')
     
      info=doctors.objects.filter(special=id,reception=False).values('id','firstname','lastname')

      data=list(info)

      return JsonResponse(data,safe=False)
     
     else:
       
       return JsonResponse({'message':'user is not authenticated'},status=401)
     
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)


# Left panel  

def leftpanel(request):

  if request.method=='GET':

    if request.user.is_authenticated :

       user=request.user.id

       role=Management.objects.get(user=user)
 
       if role.title=='Doctor':  


         info=Leftpanel.objects.filter(doctor=True).values('id','heading','icon')

         data=list(info)

         return JsonResponse(data,safe=False)
       
 
       elif role.title=='Receptionist':  

        info=Leftpanel.objects.filter(staff=True).values('id','heading','icon')

        data=list(info)

        return JsonResponse(data,safe=False)
    
       elif request.user.is_authenticated:

         info=Leftpanel.objects.filter(patient=True).values('id','heading','icon')

         data=list(info)

         return JsonResponse(data,safe=False)
   
    else:

      return JsonResponse({'message':'User is not authenticated'},status=401)
    
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)  
    
  
# for routing of panel

def panelrouting(request):

  if request.method=='GET':

    id=request.GET.get('id')
   
    info=Leftpanel.objects.get(id=id)

    return JsonResponse({'message':info.heading},status=200)   

  else:

    return JsonResponse({'message':'Method not allowed'},status=405) 


#  for prescription routing details

def prescriptiondata(request):

  if request.method=='GET':

    if request.user.is_authenticated:
     
      user=request.user.id

      role=Management.objects.get(user=user)
 
      if role.title=='Doctor':  


        id=request.GET.get('id')

        info=Appointments.objects.filter(id=id).values('id','firstname','lastname','age','gender')

        data=list(info)

        return JsonResponse(data,safe=False)
      
      else:

        return JsonResponse({'message':'Not a doctor'},status=403)
    
    else:

      return JsonResponse({'message':'User is not authenticated'},status=401)   

  else:

    return JsonResponse({'message':'Method not allowed'},status=405)  
  

  # for initiating proceess of payment by receptionist 
  
def Payment(request):

  if request.method=='POST':

   if request.user.is_authenticated :

     user=request.user.id

     role=Management.objects.get(user=user)
 
     if role.title=='Receptionist':  

       data=json.loads(request.body)

       id=data['id']
   
       fees=data['payment']

       info=Appointments.objects.get(id=id)
  
       payment.objects.create(fees=fees,appointment_id=id,firstname=info.firstname,lastname=info.lastname,gender=info.gender,age=info.age)
  
       return JsonResponse({'message':'Payment procees initiated'},status=201)
     
     else:
       
       return JsonResponse({'mesage':'Not a receptionist'},status=403)
   
   else:
     
     return JsonResponse({'message':'User is not authenticated'},status=401)
   
  else:

    return JsonResponse({'message':'Method not allowed'},status=405) 
    
  
# for payment at patient's end

def payapproval(request):

  if request.method=='PUT':

    if request.user.is_authenticated:

      data=json.loads(request.body)

      id=data['id']

      info=Appointments.objects.get(id=id)

      payment.objects.filter(appointment_id=id).update(paymentstatus=True)

      info.paystatus=True

      info.save()

      return JsonResponse({'message':'Payment Approved'},status=200)
    
    else:

      return JsonResponse({'message':'Not authenticated'},status=401)
    
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)  
  
# pdf generation of payment bill

def paymentpdf(request):

  if request.method=='GET':

    if request.user.is_authenticated:

      id=request.GET.get('id')
    
      if payment.objects.filter(appointment_id=id,paymentstatus=True).exists():

        info=payment.objects.get(appointment=id)
  
        context={
        'firstname':info.firstname,
        'lastname':info.lastname,
        'age':info.age,
        'gender':info.gender,
        'appointmentid':info.appointment_id,
        'issuetime':info.issuetime,
        'fees':info.fees
        }

        template='Management/paybase.html'

        response = HttpResponse(content_type="application/pdf")
    
        response["Content-Disposition"] = 'attachement; filename="Payment.pdf"'
                     
        render_pdf(
             template=template,
            file_=response,
            context=context,
         )
        return response
    
    
      else:

       return JsonResponse({'message':'Payment yet not done'},status=204)
     
    else:

      return JsonResponse({'message':'Not authenticated'},status=401)   
    
  else:

     return JsonResponse({'message':'Method not allowed'},status=405)  


# appointments for bill dashboard

def billdash(request):

  if request.method=='GET':

    if request.user.is_authenticated:

      user=request.user.id

      patient=Patients.objects.get(user=user)

      info=Appointments.objects.filter(patient=patient.id,docapproval=True).values('id','registerdate','firstname','medical','paystatus')

      data=list(info)

      return JsonResponse(data,safe=False)
    
    else:

      return JsonResponse({'message':'Not authenticated'},status=401) 

  else :

    return JsonResponse({'message':'Method not allowed'},status=405)  
    

#  Api for all appointment payment

def appointpayment(request):

  if request.method=='GET':

    if request.user.is_authenticated :

      user=request.user.id

      role=Management.objects.get(user=user)
 
      if role.title=='Receptionist':  

        info=Appointments.objects.filter(paystatus=False,docapproval=True).values('id','firstname','lastname','gender','age','problem')

        data=list(info)

        return JsonResponse(data,safe=False)
      
      else:

        return JsonResponse({'message':'Not a staff'},status=403)
    
    else :

      return JsonResponse({'message':'Not authenticated'},status=401)
    
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)  







  






  


  


  
 