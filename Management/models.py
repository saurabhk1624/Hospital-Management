from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    speciality=models.CharField(max_length=200)

    class Meta:

        db_table = 'staff_records'


class Patients(models.Model):

    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)

    Name=models.CharField(max_length=200)

    Phoneno=models.CharField(max_length=200) 

    Age=models.PositiveSmallIntegerField()

    problem=models.CharField(max_length=200)

    email=models.CharField(max_length=200,unique=True)

    password=models.CharField(max_length=200)

    new=models.BooleanField(default=False)

    # Gender=models.     

    class Meta:

        db_table = 'patient_records'

