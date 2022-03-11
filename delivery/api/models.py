from django.db import models
from datetime import datetime    

# Create your models here.
class Delivery(models.Model):

    class Status(models.TextChoices):
        not_picked = 'NOT_PICKED'
        picked = 'PICKED'
        delivered = 'DELIVERED'

    status = models.CharField(default= Status.not_picked,choices=Status.choices,max_length=20)    

    delivery_partner = models.BigIntegerField()   
    creation_time = models.DateTimeField(default=datetime.now())
    location_lat = models.FloatField(default=0)     #Stores latitute of location
    location_long = models.FloatField(default=0)    #Stores longitute of location
    rating = models.FloatField(default=0)
    temperature = models.FloatField(default=0)      

    #Need to store order id
                                            
    

    def __str__(self) -> str:
        return str(self.delivery_partner)

