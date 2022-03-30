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
import requests, jwt
from .interconnect import send_request_post, send_request_get
from delivery.settings import SECRET_KEY, DELIVERY_MICROSERVICE_URL, ORDERS_MICROSERVICE_URL, STORES_MICROSERVICE_URL, USERS_MICROSERVICE_URL

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
        serializer.save(delivery_partner = nearest_delivery_person.user_id, delivery_phone_no=nearest_delivery_person.phone)

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
        url = ORDERS_MICROSERVICE_URL + '/order/verifyotp/' + str(order_id)
        success, response = send_request_post(url, {'delivery_otp':otp})
        if not success:
            raise ValidationError("/order/update_status/ : Could not connect to orders microservices")
        if response.status_code == 200:
            delivery = Delivery.objects.get(order_id=order_id)
            delivery.status = delivery.Status.delivered
            delivery.save()
            return Response({"message":"Delivered"}, status=status.HTTP_200_OK)
        elif response.status_code == 400:
            return Response({"message":"Wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Matching order does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def readyToPick(request):
    order_id = request.data['order_id']
    delivery = Delivery.objects.get(order_id=order_id)
    delivery.status = delivery.Status.picked
    delivery.save()
    url = ORDERS_MICROSERVICE_URL + '/order/update_status/' + str(order_id)
    success, response = send_request_post(url, {"target_status":2})
    if not success:
        raise ValidationError("/order/update_status/ : Could not connect to orders microservices")
    print(response.status_code)
    if response.status_code != 200:
        return Response({"message": "Status could not be updated"})
    return Response({"message":"Out for delivery"})

@api_view(['GET'])
def assignedOrders(request):
    userId = jwt.decode(request.headers['Authorization'].split(' ')[-1], SECRET_KEY, algorithms=["HS256"])['id']
    print(userId)
    delivery_list= Delivery.objects.filter(delivery_partner=userId)
    deliveries=[]
    for delivery in delivery_list:
        deliveries.append({
            "delivery_id": delivery.id,
            "order_id": delivery.order_id,
            "pickup_address": delivery.pickup_address,
            "delivery_address": delivery.delivery_address,
            "status": delivery.status
        })
    
    return Response(deliveries,status=status.HTTP_200_OK)
