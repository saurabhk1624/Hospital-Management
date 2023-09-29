from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    

    pass

    class Meta:

        db_table = 'staff_records'


class Management(models.Model):

    user=models.ManyToManyField(User)

    title=models.CharField(max_length=200)

    status=models.BooleanField(default=False)

class Speciality(models.Model):

    department=models.CharField(max_length=200) 

    status=models.BooleanField(default=False) 

    class Meta:

        db_table ='department_names'  



class time(models.Model):
     
     time=models.TextField()

     status=models.BooleanField(default=False)

   
     class Meta:
         
         db_table='schedule_time'


class Leftpanel(models.Model):

    icon=models.CharField(max_length=200,default=True)

    heading=models.CharField(max_length=200)

    patient=models.BooleanField(default=False)

    staff=models.BooleanField(default=False)

    doctor=models.BooleanField(default=False)

    status=models.BooleanField(default=False)

    class Meta:

        db_table='leftpanel_records'


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

    age=models.PositiveSmallIntegerField()

    exist=models.BooleanField(default=False)

    gender=models.CharField(max_length=20)

  

    class Meta:

        db_table = 'patient_records'        


class Appointments(models.Model):

    patient=models.ForeignKey(Patients,on_delete=models.DO_NOTHING,null=True)

    doctor=models.ForeignKey(doctors,on_delete=models.DO_NOTHING,null=True)

    firstname=models.CharField(max_length=200)

    lastname=models.CharField(max_length=200)

    age=models.PositiveSmallIntegerField()

    problem=models.CharField(max_length=200)

    medical=models.TextField(null=True)

    registerdate=models.DateField()

    time=models.TextField()

    gender=models.CharField(max_length=20)

    new=models.BooleanField(default=False)

    reject=models.BooleanField(default=False)

    docapproval=models.BooleanField(default=False)

    recepapproval=models.BooleanField(default=False)

    reason=models.TextField(max_length=400,null=True)

    paystatus=models.BooleanField(default=False)

    
    class Meta:

        db_table = 'appointment_records'


class payment(models.Model) :
    
    appointment=models.ForeignKey(Appointments,on_delete=models.DO_NOTHING,null=True)

    firstname=models.CharField(max_length=200)

    lastname=models.CharField(max_length=200)

    age=models.PositiveSmallIntegerField()

    gender=models.CharField(max_length=20)

    issuetime=models.DateTimeField(auto_now_add=True)

    paymentstatus=models.BooleanField(default=False)

    fees=models.PositiveSmallIntegerField(default=0)

    class Meta:

     db_table ='payment_records'


class Prescription(models.Model):

    patient=models.ForeignKey(Patients,on_delete=models.DO_NOTHING,null=True)

    appointment=models.ForeignKey(Appointments,on_delete=models.DO_NOTHING,null=True)

    medicine_name=models.CharField(max_length=200)

    dosage=models.SmallIntegerField()

    instruction=models.TextField(null=True)

    status=models.BooleanField(default=False)


    class Meta:

        db_table='prescription_records'