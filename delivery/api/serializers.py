from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    delivery_partner = serializers.IntegerField()
    
    class Meta:
        model = Delivery
        fields = ['delivery_partner']

