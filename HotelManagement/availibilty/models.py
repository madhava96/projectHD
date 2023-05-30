from django.db import models

#creating rooms table in db for availibility purpose 
class rooms(models.Model):
    room_no=models.IntegerField(primary_key=True)
    type=models.CharField(max_length=10)
    no_of_bed=models.IntegerField()
    status=models.CharField(max_length=15)
