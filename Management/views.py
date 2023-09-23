import json

import base64
import pickle

import re

from django.http import FileResponse, JsonResponse

from Hospital import settings

from .models import Leftpanel, Patients, Speciality, User,doctors,Appointments,time

from django.contrib.auth import authenticate,login

from django.http import HttpResponse

from django.template.loader import render_to_string

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

        if not name or not email or not gender or not age or not password:
           
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
               
                  User.objects.create_user(name,email,password)

                  Id=User.objects.get(email=email)
               

                  Patients.objects.create(firstname=firstname,lastname=lastname,Age=age,gender=gender,user_id=Id.id,username=name)

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

    info=Speciality.objects.filter(Status=False).values('id','department')

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

        if not name or not email or not gender or not speciality or not password:
           
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
               
                  User.objects.create_user(name,email,password,is_superuser=True)

                  user=User.objects.get(email=email)

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

           if user.is_superuser:

            return JsonResponse({'message':'Doctor'},status=200)
          
           elif user.is_staff:

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

    patientinfo=Patients.objects.filter(user_id=user).values('username','firstname','lastname','Age','gender')

    info=list(patientinfo)

    return JsonResponse(info,safe=False)
  
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
   
  else :

    return JsonResponse({'message':'Method not allowed'},status=405) 
  

# doctor detail for doc dashboard
def doctor(request):

  if request.method=='GET':

   if request.user.is_authenticated and request.user.is_superuser:

    user=request.user.id

    patientinfo=doctors.objects.filter(user_id=user).values('username','firstname','lastname','gender')

    info=list(patientinfo)

    return JsonResponse(info,safe=False)
  
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
   
  else :

    return JsonResponse({'message':'Method not allowed'},status=405) 
  
# receptionist dashboard

def reception(request):

  if request.method=='GET':

   if request.user.is_authenticated and request.user.is_staff:

    user=request.user.id

    patientinfo=doctors.objects.filter(user_id=user).values('username','firstname','lastname','gender')

    info=list(patientinfo)

    return JsonResponse(info,safe=False)
  
   else:
     
     return JsonResponse({'message':'Not authenticated'},status=401) 
   
  else :

    return JsonResponse({'message':'Method not allowed'},status=405) 
  

# schedule time
def schedule(request):

  if request.method=='GET':

    info=time.objects.filter(status=False,capacity__lte=20).values('id','Time')

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

    time=data3['time']

    doctor=data3['doctor']
    

    user=request.user.id
    
    doc=doctors.objects.get(id=doctor)

    info=Patients.objects.get(user=user)

    if not problem or not medical or not time or doctor :

      return JsonResponse({'message':'Problem is required'},status=400)
    
    else:
      
      if Patients.objects.filter(user=user,exist=False).exists():
       
        Appointments.objects.create(firstname=info.firstname,doctor_id=doctor,lastname=info.lastname,Age=info.Age,problem=problem,gender=info.gender,Registerdate=time,medical=medical,patient_id=info.id)
        
        info.doctor_id=doctor
        
        info.exist=True

        info.save()

        return JsonResponse({'message':'Appointment applied'},status=200)
      
      else:

        Appointments.objects.create(firstname=info.firstname,doctor_id=doctor,lastname=info.lastname,Age=info.Age,problem=problem,gender=info.gender,Registerdate=time,new=True,medical=medical,patient_id=info.id)
        
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

    info=Patients.objects.all().values('user_id','firstname','lastname','Age','gender')

    patient=list(info)

    return JsonResponse(patient,safe=False)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)


# approved appointment on patient dashboard

def patientappoint(request):

  if request.method=='GET':

   if request.user.is_authenticated:

    user=request.user.id

    info=Appointments.objects.filter(user=user,patientapproval=True).values('id','firstname','lastname','Age','gender')

    appointment=list(info)

    return JsonResponse(appointment,safe=False)

   else:
     
     return JsonResponse({'message':'User is not authenticated'},status=401)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)



#All doctor record for receiption dashboard


def showdoctor(request):

  if request.method=='GET':

   if request.user.is_staff and request.user.is_authenticated:  

    info=doctors.objects.filter(reception=False).values('firstname','lastname','gender','user','speciality')

    doctor=list(info)

    return JsonResponse(doctor,safe=False)
   
   else:
     
     return JsonResponse({'message':'Not a Staff'},status=400) 
   
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# Patient under each doctor for reception  dashboard


def doctorpatients(request):

  if request.method=='GET':
    
   if request.user.is_superuser and request.user.is_authenticated: 
   
    doctorid=request.GET.get('id')

    info=Patients.objects.filter(doctor_id=doctorid).values('firstname','lastname','Age','gender')

    patients=list(info)

    return JsonResponse(patients,safe=False)
  
   else:
     
     return JsonResponse({'message':'Not a Doctor'},status=400) 
  
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# patient under each doctor for  Doctor dashboard


def doctordash(request):

  if request.method=='GET':

   if request.user.is_superuser and request.user.is_authenticated: 

    user=request.user.id
    
    data=doctors.objects.get(user=user)
   
    info=Patients.objects.filter(doctor=data.id).values('username','firstname','lastname','Age','gender')

    patients=list(info)

    return JsonResponse(patients,safe=False)
   
   else:
     
     return JsonResponse({'message':'Not a Doctor'},status=400)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# individual patient record on doctordashboard for prescription


def individualpatient(request):

  if request.method=='GET':
   
   if request.user.is_superuser and request.user.is_authenticated:


    patientid=request.GET.get('patientid')

    info=Patients.objects.filter(id=patientid).values('firstname','lastname','Age','gender')

    patient=list(info)

    return JsonResponse(patient,safe=False)
   
   else:
     
     return JsonResponse({'message':'Not a Doctor'},status=400)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  

# approval of appointment from receptionist

def recepapproval(request):

  if request.method=='PUT':
   
   if request.user.is_staff and request.user.is_authenticated:

    data=json.loads(request.body)

    appointid=data['id']

    Appointments.objects.filter(id=appointid).update(docapproval=True)

    info=Appointments.objects.get(id=appointid)
      
    
    loads=Patients.objects.get(id=info.patient_id)

    email=User.objects.get(id=loads.user_id)
    

    Doc=doctors.objects.get(id=loads.doctor_id)


    data={
       'Appointmentno':info.id,
       'Firstname':info.firstname,
       'Lastname':info.lastname,
       'Age':info.Age,
       'Problem':info.problem,
       'Gender':info.gender,
       'Doctor':Doc.firstname,
        'Time':info.Registerdate
       }
    subject='Regarding Appointment Status'

    from_email=settings.EMAIL_HOST_USER

    to_list=[email.email,]
     
    m='Your Appointment has been approved'

    message=render_to_string('Management/email.html',context=data)


    send_mail(subject,message=m,from_email=from_email,recipient_list=to_list,html_message=message,fail_silently=False)

    return JsonResponse({'message':'Appointment approved'},status=200)
   
   else:
     
     return JsonResponse({'message':'Not a Staff'},status=400) 
  
  elif request.method=='DELETE':

   if request.user.is_staff and request.user.is_authenticated:
    
    data1=json.loads(request.body)

    appointid=data1['id']

    Appointments.objects.filter(id=appointid).update(reject=True)

    return JsonResponse({'message':'Appointment rejected'},status=200)
   
   else:
     
     return JsonResponse({'message':'Not a Staff'},status=400) 
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)

# all appointment for reception dashboard


def recepappoint(request):

    if request.method=='GET':
      
     if request.user.is_staff and request.user.is_authenticated:

      info=Appointments.objects.filter(new=False).values('id','firstname','lastname','Age','problem','gender')

      patient=list(info)

      return JsonResponse(patient,safe=False)
     
     else:
     
      return JsonResponse({'message':'Not a Doctor'},status=400)  
    
    else :

      return JsonResponse({'message':'Method not allowed'},status=405)
    

# all appointment for doctor dashboard


def docappoint(request):

  if request.method=='GET':

   if request.user.is_superuser and request.user.is_authenticated:

    info=Appointments.objects.filter(new=True).values('id','firstname','lastname','Age','problem','gender')

    patient=list(info)

    return JsonResponse(patient,safe=False)
   
   else:
     
     return JsonResponse({'message':'Not a Doctor'},status=400) 
  
  else :

    return JsonResponse({'message':'Method not allowed'},status=405)
  

# pdf generation of appointment

def render_app(request):

    if request.method=='GET':
     
     appointid=request.GET.get('id')
     
     info=Appointments.objects.get(id=appointid)
      
    
     loads=Patients.objects.get(id=info.patient_id)


     Doc=doctors.objects.get(id=loads.doctor_id)


     data={
       'Appointmentno':info.id,
       'Firstname':info.firstname,
       'Lastname':info.lastname,
       'Age':info.Age,
       'Problem':info.problem,
       'Gender':info.gender,
       'Doctor':Doc.firstname

       }
    
     p=render_to_string('Management/Appoint.html',context=data)
    
     response = HttpResponse(content_type='application/templates/pdf')
    
     response['Content-Disposition'] = 'attachement; filename="Appointment.pdf"'
     
     response.write(p)
     
     return response

def  prescription(request):

  if request.method=='PUT':
    
    if request.user.is_authenticated and request.user.is_superuser:

     loads=json.loads(request.body)

     id=loads['id']

     prescription=loads['prescription']
     
     if not prescription:
       
       return JsonResponse({'message':'Precription allowed'},status=400)
     
     else:
       
       Appointments.objects.filter(id=id).update(prescription=prescription)

       return JsonResponse({'message':'Prescription added'},status=200)
     
    else :

      return JsonResponse({'message':'User is not doctor'},status=403)
    
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)


def prescriptionpdf(request):

  if request.method=='GET':
   
   if request.user.is_authenticated:
     
     id=request.GET.get('id')

     info=Appointments.objects.get(id=id)
      
     data={
       'Appointmentno':info.id,
       'Firstname':info.firstname,
       'Lastname':info.lastname,
       'Age':info.Age,
       'Problem':info.problem,
       'Gender':info.gender,
       'prescription':info.prescription
       }
     
     p=render_to_string('Management/prescription.html',context=data)
     
     response = HttpResponse(content_type='application/templates/pdf')
    
     response['Content-Disposition'] = 'filename="Prescription.pdf"'

     response.write(p)

     return response
   
  # dependent dropdown doctor list

def doctorlist(request):
  
  if request.method=='GET':
    
     if request.user.is_authenticated:
    
      id=request.GET.get('id')
     
      info=doctors.objects.filter(special=id).values('id','firstname','lastname')

      data=list(info)

      return JsonResponse(data,safe=False)
     
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  
# Left panel  

def leftpanel(request):

  if request.method=='GET':

    if request.user.is_authenticated and request.user.is_superuser:

      info=Leftpanel.objects.filter(Staff=True).values('id','Heading')

      data=list(info)

      return JsonResponse(data,safe=False)
   
    elif request.user.is_authenticated and request.user.is_staff:

      info=Leftpanel.objects.all().values('id','Heading')

      data=list(info)

      return JsonResponse(data,safe=False)
    
    elif request.user.is_authenticated:

      info=Leftpanel.objects.filter(Patient=True).values('id','Heading')

      data=list(info)

      return JsonResponse(data,safe=False)
   
    else:

      return JsonResponse({'message':'User is not authenticated'},status=401)
    
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)  
    
    
















     
  



  






  


  


  
 