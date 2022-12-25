from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from email.mime import image
from email.policy import default

asset_type_choices=[('LAPTOP','LAPTOP'),('PACKAGE','PACKAGE'),('TRAVEL_BAG','TRAVEL_BAG')]
asset_sensitivity_choices=[('HIGHLY SENSITIVE','HIGHLY SENSITIVE'),('SENSITIVE','SENSITIVE'),('NORMAL','NORMAL')]
travel_medium_choices=[('BUS','BUS'),('CAR','CAR'),('TRAIN','TRAIN')]
asset_status_choices=[('PENDING','PENDING'),('EXPIRED','EXPIRED')]

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    type=models.CharField(max_length=15)
    
    def __str__(self):        
        return (f"{self.user.username}'s Profile ")

# Create your models here.




class AssetRequest(models.Model):
    transport_from=models.CharField(max_length=100)
    transport_to=models.CharField(max_length=100)
    time=models.DateTimeField()
    flexible_timings=models.BooleanField()    
    asset_type=models.CharField(max_length=15,choices=asset_type_choices)
    asset_sensitivity=models.CharField(max_length=25,choices=asset_sensitivity_choices)
    asset_quantity=models.IntegerField()
    status=models.CharField(max_length=15,default='PENDING',choices=asset_status_choices)
    deliver_to=models.CharField(max_length=100)    
    requester=models.ForeignKey(User,on_delete=models.CASCADE)

    
    

class TravelInfo(models.Model):
    transport_from=models.CharField(max_length=100)
    transport_to=models.CharField(max_length=100)
    time=models.DateTimeField()
    flexible_timings=models.BooleanField()
    travel_medium=models.CharField(max_length=15,choices=travel_medium_choices)    
    asset_quantity=models.IntegerField()    
    rider=models.ForeignKey(User,on_delete=models.CASCADE)
    applicants=models.ManyToManyField(AssetRequest,related_name="rides")
    
    