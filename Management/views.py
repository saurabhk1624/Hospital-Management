import json

import re

from django.http import JsonResponse

from .models import Patients, User,doctors,Appointments

from django.contrib.auth import authenticate,login



# Registartion of patient

def patientregister(request):

    if request.method=='POST':

        data=json.loads(request.body)

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

          if User.objects.filter(email=email).exists():
           
           return JsonResponse({'message':'Email already exist'},status=400)
          
          else: 
           
           if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,15}$",password) is None:
             
             return JsonResponse({'message':'Password denied: Password is not valid'},status=400)
           
           else:
              
              if cpassword==password:
               
               User.objects.create_user(name,email,password)
               Id=User.objects.get(email=email)

               Patients.objects.create(name=name,Age=age,gender=gender,user_id=Id.id)

               return JsonResponse({'message':'Registration Successful'},status=200)
              
              else:

                return JsonResponse({'message':'Confirm Password not same'},status=401)
              
    else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
    


#  login of patient       

def patientlogin(request):
  
  if request.method=='POST':
     
     data1=json.loads(request.body)

     username= data1['username']

     password =data1['password']

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
    
        name=data2['name']

        gender=data2['gender']

        email=data2['email']

        speciality=data2['speciality']

        password=data2['password']

        cpassword=data2['confirmpassword']

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
               
               User.objects.create_user(name,email,password)

               user=User.objects.get(email=email)

               doctors.objects.create(name=name,gender=gender,speciality=speciality,user_id=user.id)



               return JsonResponse({'message':'Registration Successful'},status=200)
              
              else:

                return JsonResponse({'message':'Confirm Password not same'},status=401)
              
  else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
  


# login of staff 
 
    
def stafflogin(request):

   if request.method=='POST':
     
     data1=json.loads(request.body)

     username= data1['username']

     password =data1['password']

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

    user=request.user.id

    patientinfo=Patients.objects.filter(id=user).values('name','Age','gender')

    info=list(patientinfo)

    return JsonResponse(info,safe=False)



# for Appointment


def appointment(request):

  if request.method=='POST':

    data3=json.loads(request)

    problem=data3['problem']

    medical=data3['medical']

    time=data3['time']

    user=request.user.id

    info=Patients.objects.get(user_id=user)

    if not problem:

      return JsonResponse({'message':'Problem is required'},status=400)
    
    else:
      
      if Patients.objects.filter(user_id=user,new=False).exists():
       
        Appointments.objects.create(name=info.name,Age=info.Age,problem=problem,gender=info.gender,medicalhistory=medical,time=time)

        info.exist=True

        info.save()

        return JsonResponse({'message':'Appointment applied'},status=200)
      
      else:

        Appointments.objects.create(name=info.name,Age=info.Age,problem=problem,gender=info.gender,new=True)

        return JsonResponse({'message':'Appointment applied'},status=200)
      
  else :

    return JsonResponse({'message':'Method not allowed'},status=405)  
  


# All Patient record for reception dashboard


def showpatient(request):

  if request.method=='GET':

    info=Patients.objects.all().values('user_id','name','Age','Gender')

    patient=list(info)

    return JsonResponse(patient,safe=False)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)



#All doctor record for receiption dashboard


def showdoctor(request):

  if request.method=='GET':

    info=doctors.objects.all().values('name','Gender','user_id','speciality')

    doctor=list(info)

    return JsonResponse(doctor,safe=False)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# Patient under each doctor for reception  dashboard


def doctorpatients(request):

  if request.method=='GET':

    data=json.loads(request.body)

    doctorid=data['id']

    info=Patients.objects.filter(doctorid=doctorid).values('name','Age','gender')

    patients=list(info)

    return JsonResponse(patients,safe=False)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# patient under each doctor for  Doctor dashboard


def doctordash(request):

  if request.method=='GET':

    user=request.user.id

    info=Patients.objects.filter(doctorid=user).values('name','Age','gender')

    patients=list(info)

    return JsonResponse(patients,safe=False)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  


# individual patient record on doctordashboard for prescription


def individualpatient(request):

  if request.method=='GET':

    data=json.loads(request.body)

    patientid=data['patientid']

    info=Patients.objects.filter(id=patientid).values('name','Age','gender')

    patient=list(info)

    return JsonResponse(patient,safe=False)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)
  






  


  


  

  











    
    
    


    











