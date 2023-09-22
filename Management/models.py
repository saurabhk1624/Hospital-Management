from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    

    pass

    class Meta:

        db_table = 'staff_records'




class Speciality(models.Model):

    department=models.CharField(max_length=200) 

    Status=models.BooleanField(default=False) 

    class Meta:

        db_table ='department_names'  



class time(models.Model):
     
     Time=models.TextField()
     status=models.BooleanField(default=False)
     capacity=models.PositiveSmallIntegerField()

     class Meta:
         
         db_table='schedule_time'


# class Navbar(models.Model):

#     Headings=models.CharField(max_length=200)

#     status=models.BooleanField(default=False)


class doctors(models.Model):
      
      special=models.ForeignKey(Speciality,on_delete=models.DO_NOTHING)

      time=models.ForeignKey(time,on_delete=models.DO_NOTHING,null=True)

      user=models.ForeignKey(User,on_delete=models.DO_NOTHING)

      username=models.CharField(max_length=200)

      firstname=models.CharField(max_length=200)

      lastname=models.CharField(max_length=200)

      gender=models.CharField(max_length=20)

      reception=models.BooleanField(default=False)

      speciality=models.CharField(max_length=200)

      class Meta:

        db_table = 'doctors_records'

class Patients(models.Model):

    user=models.ForeignKey(User,on_delete=models.DO_NOTHING) 
    
    doctor=models.ForeignKey(doctors,on_delete=models.DO_NOTHING,null=True)

    username=models.CharField(max_length=200)

    firstname=models.CharField(max_length=200)

    lastname=models.CharField(max_length=200)

    Age=models.PositiveSmallIntegerField()

    exist=models.BooleanField(default=False)

    gender=models.CharField(max_length=20)

  

    class Meta:

        db_table = 'patient_records'        


class Appointments(models.Model):

    patient=models.ForeignKey(Patients,on_delete=models.CASCADE)

    doctor=models.ForeignKey(doctors,on_delete=models.DO_NOTHING,null=True)

    firstname=models.CharField(max_length=200)

    lastname=models.CharField(max_length=200)

    Age=models.PositiveSmallIntegerField()

    problem=models.CharField(max_length=200)

    medical=models.TextField(null=True)

    Registerdate=models.DateField()

    gender=models.CharField(max_length=20)

    new=models.BooleanField(default=False)

    reject=models.BooleanField(default=False)

    patientapproval=models.BooleanField(default=False)

    docapproval=models.BooleanField(default=False)

    prescription=models.TextField(max_length=400,null=True)

    reason=models.TextField(max_length=400,null=True)

    

    class Meta:

        db_table = 'appointment_records'


class payment(models.Model) :

    appointment=models.ForeignKey(Appointments,on_delete=models.CASCADE)

    name=models.CharField(max_length=200)

    Age=models.PositiveSmallIntegerField()

    gender=models.CharField(max_length=20)

    issuetime=models.DateField(auto_now_add=True)

    class Meta:

     db_table ='payment_records'


# class medical(models.Model):

#     appointment=models.ForeignKey()