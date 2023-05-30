from django.db import models

#creating tables for username and pass for login purpose
class login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
