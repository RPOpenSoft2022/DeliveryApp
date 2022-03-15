from api.serializers import DeliverySerializer, DeliveryUserSerializer
from . models import Delivery,DeliveryUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.gis.db.models.functions import Distance
import requests

class DeliveryViewsets(viewsets.ModelViewSet):
    queryset=Delivery.objects.all()
    serializer_class=DeliverySerializer
    permission_classes=[]

class DeliveryUserViewsets(viewsets.ModelViewSet):
    queryset=DeliveryUser.objects.all()
    serializer_class=DeliveryUserSerializer
    permission_classes=[]

    def perform_create(self, serializer):

        delivery_pickup_location = serializer.data['pickup_location']

        delivery_persons_queryset = DeliveryUser.objects.annotate(
            distance = Distance('current_location', delivery_pickup_location)
        ).order_by('distance')   

        nearest_delivery_person = delivery_persons_queryset.first()

        serializer.save(delivery_partner = nearest_delivery_person.id)
