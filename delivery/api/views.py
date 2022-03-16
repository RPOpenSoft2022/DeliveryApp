from django.http import HttpResponse
from api.serializers import * 
from . models import Delivery,DeliveryUser
from rest_framework.decorators import api_view
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

class getDeliveryOTP(viewsets.ViewSet):
    queryset=Delivery.objects.all()
    serializer_class=OTPSerializer

    def create(self,request):
        order_id=request.data['order_id']
        otp=request.data['otp']
        print(order_id,otp)
        response=requests.post(url='http://localhost:3001/order/verifyotp/{order_id}',data = {'delivery_otp':otp})
        if(response.status_code==200):
            delivery = Delivery.objects.get(order_id=order_id)
            delivery.status = delivery.status[2]
            delivery.save()
            return Response({"message":"Delivered"})
        else:
            return Response({"message":"wrong OTP"})


@api_view(['PUT'])
def readyToPick(request):
    order_id=request.POST.get('order_id')
    delivery = Delivery.objects.get(order_id=order_id)
    delivery.status = delivery.status[1]
    delivery.save()
    requests.post(url='localhost:8000/order/update_status/'+order_id, json={"target_status":2})
    return Response({"message":"out for delivery"})