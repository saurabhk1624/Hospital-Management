from django.db import models

from django.contrib.auth.models import User

class Users(User):

    
    class Meta:

        db_table = 'user_records'


class Patients(models.Model):

    Name=models.CharField(max_length=200)

    Phoneno=models.CharField() 

    Age=models.PositiveSmallIntegerField()

    # Gender=models.     


