import json

import re

from django.http import JsonResponse

from .models import Patients, User,doctors,Appointments

from django.contrib.auth import authenticate,login

from django.http import HttpResponse

from django_renderpdf.views import PDFView

# from reportlab.pdfgen import canvas 

# from django.http import HttpResponse  
      


# def getpdf(request): 
         
#         if request.method=='GET':

#          response = HttpResponse(content_type='application/pdf')  
#          response['Content-Disposition'] = 'attachment; filename="file.pdf"'  
#          p = canvas.Canvas(response)  
#          p.setFont("Times-Roman", 55)  
#          p.drawString(100,700, "Hello, Saurabh.")  
#          p.showPage()  
#          p.save()  
#          return response  





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

        firstname=data2['firstname']

        lastname=data2['lastname']

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
               
                if User.objects.filter(username=name).exists():
       
                    return JsonResponse({'message':'usrname already exist'},status=400)
       
                else:
               
                  User.objects.create_user(name,email,password,is_superuser=True)

                  user=User.objects.get(email=email)

                  doctors.objects.create(firstname=firstname,lastname=lastname,gender=gender,speciality=speciality,user_id=user.id,username=name)
               

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
  



# for Appointment


def appointment(request):

  if request.method=='POST':

   if request.user.is_authenticated: 

    data3=json.loads(request.body)

    problem=data3['problem']

    medical=data3['medical']

    time=data3['time']

    user=request.user.id

    info=Patients.objects.get(user_id=user)

    if not problem or not medical :

      return JsonResponse({'message':'Problem is required'},status=400)
    
    else:
      
      if Patients.objects.filter(user_id=user,exist=False).exists():
       
        Appointments.objects.create(firstname=info.firstname,lastname=info.lastname,Age=info.Age,problem=problem,gender=info.gender,Registerdate=time,medical=medical,user_id=user)

        info.exist=True

        info.save()

        return JsonResponse({'message':'Appointment applied'},status=200)
      
      else:

        Appointments.objects.create(firstname=info.firstname,lastname=info.lastname,Age=info.Age,problem=problem,gender=info.gender,Registerdate=time,new=True,medical=medical,user_id=user)

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

    info=Appointments.objects.filter(user_id=user,approve=True).values('id','firstname','lastname','Age','gender')

    appointment=list(info)

    return JsonResponse(appointment,safe=False)

   else:
     
     return JsonResponse({'message':'User is not authenticated'},status=401)
  
  else:

    return JsonResponse({'message':'Method not allowed'},status=405)



#All doctor record for receiption dashboard


def showdoctor(request):

  if request.method=='GET':

   if request.user.is_superuser and request.user.is_authenticated:  

    info=doctors.objects.all().values('firstname','lastname','Gender','user_id','speciality')

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
   
    data=json.loads(request.body)

    doctorid=data['id']

    info=Patients.objects.filter(doctorid=doctorid).values('firstname','lastname','Age','gender')

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

    info=Patients.objects.filter(doctorid=user).values('username','firstname','lastname','Age','gender')

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

    data=json.loads(request.body)

    patientid=data['patientid']

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

    Appointments.objects.filter(id=appointid).update(approve=True)

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
   
     pdf_content = "Hello, this is a PDF generated without templates!"

     response = HttpResponse(content_type='application/pdf')

    #  response['Content-Disposition'] = 'filename="example.pdf"'

    #  response = HttpResponse(pdf. read(), content_type='application/pdf')
    
     response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
    
     PDFView(response, pdf_content,prompt_download = True)

     return response








  






  


  


  

  











    
    
    


    











