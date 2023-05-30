from django.db import models
import os
from django.db.models.deletion import CASCADE
from django.db.models.base import Model
import MySQLdb as sql

# Create your models here.

class logindetails(models.Model):
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role=models.CharField(max_length=20)
    mail=models.EmailField(max_length=30)

def upload_path(instance, filename):
    # change the filename here is required
    return os.path.join("uploads", filename)


class clientdetails(models.Model):
    clientname=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    password=models.BinaryField(max_length=100)
    def _enc(self, value):  #this function encrypt the password
       conn = sql.connect(user='root',passwd='root',db='marketing')
       cur = conn.cursor()
       cur.execute("SELECT AES_ENCRYPT('{}','pass')".format(value))
       return cur.fetchone()[0]
    
    email=models.CharField(max_length=100)
    date=models.CharField(max_length=50)
    image=models.ImageField(upload_to=upload_path)
    role = models.CharField(max_length=20)


class requirements(models.Model):
    deptid  = models.ForeignKey(clientdetails,on_delete=CASCADE)
    name = models.CharField(max_length=100)
    
    campaign_name = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    planned_impressions = models.CharField(max_length=100)
    planned_cpm = models.CharField(max_length=100)
    planned_cpc = models.CharField(max_length=100)
    planned_cost = models.CharField(max_length=100)

class user_report(models.Model):
    clientname = models.CharField(max_length=100)
    campaign_name = models.CharField(max_length=100)
    date=models.CharField(max_length=10)
    no_of_impressions=models.IntegerField()
    no_of_clicks=models.IntegerField()
    cost_per_impressions=models.FloatField()
    cost_per_click=models.FloatField()
    total_cost_per_impressions=models.FloatField()
    total_cost_per_click=models.FloatField()
    cost_per_day=models.FloatField()
    clientid = models.ForeignKey(requirements,on_delete=CASCADE)
