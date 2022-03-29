from django.http import HttpResponse
from api.serializers import * 
from . models import Delivery,DeliveryUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import viewsets
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import requests
from .interconnect import send_request_post, send_request_get
from delivery.settings import DELIVERY_MICROSERVICE_URL, ORDERS_MICROSERVICE_URL, STORES_MICROSERVICE_URL, USERS_MICROSERVICE_URL


def isNumber(n):
    if n is None:
        return False
    try:
        return float(n)
    except:
        return False

class DeliveryViewsets(viewsets.ModelViewSet):
    queryset=Delivery.objects.all()
    serializer_class=DeliverySerializer
    permission_classes=[]

    def perform_create(self, serializer):
        delivery_pickup_location = Point(isNumber(self.request.data['pickup_location']['latitude']), isNumber(self.request.data['pickup_location']['longitude']), srid=4326)

        delivery_persons_queryset = DeliveryUser.objects.annotate(
            distance = Distance('current_location', delivery_pickup_location)
        ).order_by('distance')   
        
        nearest_delivery_person = delivery_persons_queryset.first()
        serializer.save(delivery_partner = nearest_delivery_person.user_id)

class DeliveryUserViewsets(viewsets.ModelViewSet):
    queryset=DeliveryUser.objects.all()
    serializer_class=DeliveryUserSerializer
    permission_classes=[]



class getDeliveryOTP(viewsets.ViewSet):
    queryset=Delivery.objects.all()
    serializer_class=OTPSerializer

    def create(self,request):
        order_id=request.data['order_id']
        otp=request.data['otp']
        print(order_id,otp)
        url = ORDERS_MICROSERVICE_URL + '/order/verifyotp/' + order_id
        success, response = send_request_post(url, {'delivery_otp':otp})
        if not success:
            raise ValidationError("/order/update_status/ : Could not connect to orders microservices")
        if(response.status_code==200):
            delivery = Delivery.objects.get(order_id=order_id)
            delivery.status = delivery.status[2]
            delivery.save()
            return Response({"message":"Delivered"})
        else:
            return Response({"message":"Wrong OTP"})


@api_view(['POST'])
def readyToPick(request):
    order_id = request.data['order_id']
    delivery = Delivery.objects.get(order_id=order_id)
    delivery.status = delivery.status[1]
    delivery.save()
    url = ORDERS_MICROSERVICE_URL + '/order/update_status/' + order_id
    success, response = send_request_post(url, {"target_status":2})
    if not success:
        raise ValidationError("/order/update_status/ : Could not connect to orders microservices")
    return Response({"message":"Out for delivery"})