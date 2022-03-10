from rest_framework import serializers


class DeliverySerializer(serializers.Serializer):
    delivery_partner = serializers.IntegerField()

