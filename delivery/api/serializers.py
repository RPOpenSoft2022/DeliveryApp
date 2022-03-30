from rest_framework import serializers
from .models import Delivery, DeliveryUser
from drf_extra_fields.geo_fields import PointField

class DeliverySerializer(serializers.ModelSerializer):
    pickup_location = PointField()

    class Meta:
        model = Delivery
        fields = ['id','delivery_partner', 'delivery_phone_no','creation_time','pickup_location','rating','temperature','status','pickup_address','delivery_address', 'customer_name', 'customer_phone_number','order_id','order_details']


class DeliveryUserSerializer(serializers.ModelSerializer):
    
    current_location = PointField()

    class Meta:
        model = DeliveryUser
        fields = ['id','name','phone','email','user_id','current_location','last_updated_location_time','is_free']

class OTPSerializer(serializers.Serializer):
    order_id=serializers.IntegerField()
    otp=serializers.IntegerField()

