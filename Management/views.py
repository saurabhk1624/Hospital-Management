import json

import re

from django.http import JsonResponse

from .models import Patients, User

from django.contrib.auth import authenticate,login



def patientregister(request):

    if request.method=='POST':

        data=json.loads(request.body)

        name=data['name']

        age=data['age']

        email=data['email']

        problem=data['problem']

        password=data['password']

        cpassword=data['confirmpassword']

        doctor=User.objects.get(speciality=problem)

        # Id=doctor.id

        if not name or not email:
           
           return JsonResponse({'message':'All fields are required'},status=400)
     
        else:
         
         if not  re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email) :
           
           return JsonResponse({'message':'Not valid Email'},status=400)
         
         else:

          if Patients.objects.filter(email=email).exists():
           
           return JsonResponse({'message':'Email already exist'},status=400)
          
          else: 
           
           if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,15}$",password) is None:
             
             return JsonResponse({'message':'Password denied: Password is not valid'},status=400)
           
           else:
              
              if cpassword==password:
               
               Patients.objects.create_user(name,email,password,age,problem)

               return JsonResponse({'message':'Registration Successful'},status=200)
              
              else:

                return JsonResponse({'message':'Confirm Password not same'},status=401)
              
    else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
    

def patientlogin(request):
  
  if request.method=='POST':
     
     data1=json.loads(request.body)

     email= data1['email']

     password =data1['password']

     user = authenticate(email=email, password=password)

     if user  is not None:
        
          login(request,user)
          

          return JsonResponse({'message':'Logged in'},status=200)
        
     else:
       
       return JsonResponse({'message':'username or password is  not same'},status=400)
     
  else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
  


def staffregister(request):

  if request.method=='POST':

        data2=json.loads(request.body)
    
        name=data2['name']

        email=data2['email']

        speciality=data2['speciality']

        password=data2['password']

        cpassword=data2['confirmpassword']

        if not name or not email:
           
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
               
               User.objects.create_user(name,email,password,speciality)

               return JsonResponse({'message':'Registration Successful'},status=200)
              
              else:

                return JsonResponse({'message':'Confirm Password not same'},status=401)
              
  else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
    
def stafflogin(request):

   if request.method=='POST':
     
     data1=json.loads(request.body)

     email= data1['email']

     password =data1['password']

     user = authenticate(email=email, password=password)

     if user  is not None:
        
          login(request,user)

          if user.is_superuser:

           return JsonResponse({'message':'Admin'},status=200)
          
          else :

            return JsonResponse({'message':'Stafflogin'},status=200)

     else:
       
       return JsonResponse({'message':'username or password is  not same'},status=400)
     
   else:
      
      return JsonResponse({'message':'Method not allowed'},status=405)
    


def appointments(request):


  

  return JsonResponse({'message':'Appointment registered successfully'})

    
