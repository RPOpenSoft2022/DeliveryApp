from rest_framework import serializers
from .models import Delivery, DeliveryUser

class DeliverySerializer(serializers.ModelSerializer):
    delivery_partner = serializers.IntegerField()
    
    class Meta:
        model = Delivery
        fields = ['delivery_partner','creation_time','delivery_location_lat','delivery_location_long','pickup_location_lat','pickup_location_long','rating','temperature','status','pickup_address','delivery_address','customer_phone_number','order_id','order_details']


class DeliveryUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DeliveryUser
        fields = ['user_id','current_lat','current_long','last_updated_location_time','is_free']