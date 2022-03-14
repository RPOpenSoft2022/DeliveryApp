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
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    location_lat = models.FloatField(default=0)     #Stores latitute of location
    location_long = models.FloatField(default=0)    #Stores longitute of location
    rating = models.FloatField(default=0)
    temperature = models.FloatField(default=0)     
    pickup_address = models.TextField(default='')
    delivery_address = models.TextField(default='')
    customer_phone_number = models.TextField(default='')
    order_id = models.BigIntegerField(null=True)
    order_details = models.TextField(default='') 

                                            
    

    def __str__(self) -> str:
        return str(self.delivery_partner)

