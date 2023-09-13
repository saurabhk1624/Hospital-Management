from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    pass

    class Meta:

        db_table = 'staff_records'


class Patients(models.Model):

    user=models.ForeignKey(User,on_delete=models.DO_NOTHING) 

    name=models.CharField(max_length=200)

    Age=models.PositiveSmallIntegerField()

    exist=models.BooleanField(default=False)

    gender=models.CharField(max_length=20)

    doctor=models.CharField(max_length=200,null=True)

    class Meta:

        db_table = 'patient_records'


class doctors(models.Model):

      user=models.ForeignKey(User,on_delete=models.DO_NOTHING)

      name=models.CharField(max_length=200)

      speciality=models.CharField(max_length=200)

      gender=models.CharField(max_length=20)

      class Meta:

        db_table = 'doctors_records'


class Appointments(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)

    name=models.CharField(max_length=200)

    Age=models.PositiveSmallIntegerField()

    problem=models.CharField(max_length=200)

    Registerdate=models.DateField()

    gender=models.CharField(max_length=20)

    new=models.BooleanField(default=False)

    reject=models.BooleanField(default=False)

    patientapproval=models.BooleanField(default=False)

    docapproval=models.BooleanField(default=False)

    prescription=models.TextField(max_length=400,null=True)

    medicalhistory=models.TextField(max_length=400,null=True)


    class Meta:

        db_table = 'appointment_records'


class payment(models.Model) :

    appointment=models.ForeignKey(Appointments,on_delete=models.CASCADE)

    name=models.CharField(max_length=200)

    Age=models.PositiveSmallIntegerField()

    gender=models.CharField(max_length=20)

    issuetime=models.DateField(auto_now_add=True)

    doctorname=models.CharField(max_length=200)