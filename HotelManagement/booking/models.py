from django.db import models
from availibilty.models import rooms

# creating table for booking purpose
class booking(models.Model):
    sr_no = models.AutoField(primary_key=True)
    a_room=models.ForeignKey(rooms,on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=80)
    mobile_no=models.BigIntegerField()
    email=models.CharField(max_length=100)
    checkin=models.DateField()
    checkout=models.DateField()

