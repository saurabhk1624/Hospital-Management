from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    

    pass

    class Meta:

        db_table = 'staff_records'


class Patients(models.Model):

    user=models.ForeignKey(User,on_delete=models.DO_NOTHING) 

    firstname=models.CharField(max_length=200)

    lastname=models.CharField(max_length=200)

    Age=models.PositiveSmallIntegerField()

    exist=models.BooleanField(default=False)

    gender=models.CharField(max_length=20)

    doctor=models.CharField(max_length=200,null=True)

    class Meta:

        db_table = 'patient_records'


class doctors(models.Model):

      user=models.ForeignKey(User,on_delete=models.DO_NOTHING)

      firstname=models.CharField(max_length=200)

      lastname=models.CharField(max_length=200)

      speciality=models.CharField(max_length=200)

      gender=models.CharField(max_length=20)

      class Meta:

        db_table = 'doctors_records'


class Appointments(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)

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