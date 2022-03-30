from email.policy import default
from django.contrib.gis.db import models


class Delivery(models.Model):

    class Status(models.TextChoices):
        not_picked = 'NOT_PICKED'
        picked = 'PICKED'
        delivered = 'DELIVERED'

    status = models.CharField(default= Status.not_picked,choices=Status.choices,max_length=20)    

    delivery_partner = models.BigIntegerField(blank=True) 
    delivery_phone_no = models.BigIntegerField(blank=True, null=True)  
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    pickup_location = models.PointField(null=True)

    rating = models.FloatField(default=0)
    temperature = models.FloatField(default=0)     
    pickup_address = models.TextField(default='')
    delivery_address = models.TextField(default='')
    customer_name = models.CharField(max_length=100, blank=True)
    customer_phone_number = models.TextField(default='')
    order_id = models.BigIntegerField(null=True, unique=True)
    order_details = models.TextField(default='') 


    def __str__(self) -> str:
        return str(self.order_id)



class DeliveryUser(models.Model):

        name = models.TextField(blank=True)
        phone = models.TextField(blank=True)
        email = models.EmailField(blank=True)
        user_id = models.BigIntegerField()

        current_location = models.PointField(null=True)

        last_updated_location_time = models.DateTimeField(verbose_name="Last updated location time", null=True, blank=True)
        is_free = models.BooleanField(default=True)

        def __str__(self) -> str:
            return str(self.user_id)




