from email.policy import default
from django.db import models
from datetime import datetime   
from django_json_api.models import JSONAPIModel
from django_json_api.fields import Attribute
from django_json_api.django import RelatedJSONAPIField


class Delivery(models.Model):

    class Status(models.TextChoices):
        not_picked = 'NOT_PICKED'
        picked = 'PICKED'
        delivered = 'DELIVERED'

    status = models.CharField(default= Status.not_picked,choices=Status.choices,max_length=20)    

    delivery_partner = models.BigIntegerField()   
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    pickup_location_lat = models.FloatField(default=0)     #Stores latitute of location
    pickup_location_long = models.FloatField(default=0)    #Stores longitute of location
    delivery_location_lat = models.FloatField(default=0)
    delivery_location_long = models.FloatField(default=0)
    rating = models.FloatField(default=0)
    temperature = models.FloatField(default=0)     
    pickup_address = models.TextField(default='')
    delivery_address = models.TextField(default='')
    customer_phone_number = models.TextField(default='')
    order_id = models.BigIntegerField(null=True)
    order_details = models.TextField(default='') 


    def __str__(self) -> str:
        return str(self.delivery_partner)


class MyUser(JSONAPIModel):
    class Meta:
        # api_url = MICROSERVICE_A_API_URL
        resource_type = 'user'

    name = Attribute()
    phone = Attribute()
    email = Attribute()

class DeliveryUser(models.Model):

       # user_info = RelatedJSONAPIField(json_api_model=MyUser,default='')
        user_id = models.BigIntegerField()
        current_lat = models.DecimalField(verbose_name="Current Latitude",max_digits=22,
    decimal_places=16, null=True, blank=True)
        current_long= models.DecimalField(verbose_name="Current Longitude",max_digits=22,
    decimal_places=16, null=True, blank=True)
        last_updated_location_time = models.DateTimeField(verbose_name="Last updated location time", null=True, blank=True)
        is_free = models.BooleanField(default=True)

        def __str__(self) -> str:
            return str(self.user_id)




