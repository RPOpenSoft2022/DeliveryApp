from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    delivery_partner = serializers.IntegerField()
    
    class Meta:
        model = Delivery
        fields = ['delivery_partner','creation_time','location_lat','location_long','rating','temperature','status','pickup_address',' delivery_address','customer_phone_number',' order_id','order_details']

