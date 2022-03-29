from django.http import HttpResponse
from api.serializers import * 
from . models import Delivery,DeliveryUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import requests
import jwt
from delivery.settings import SECRET_KEY 

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

        # delivery_pickup_location = serializer.data['pickup_location']
        delivery_pickup_location = Point(isNumber(self.request.data['pickup_location']['latitude']), isNumber(self.request.data['pickup_location']['longitude']), srid=4326)

        delivery_persons_queryset = DeliveryUser.objects.annotate(
            distance = Distance('current_location', delivery_pickup_location)
        ).order_by('distance')   
        
        # users = DeliveryUser.objects.all()
        # closest_first = (Distance(delivery_pickup_location, users[0].current_location), users[0].user_id)
        # for user in users:
        #    if(Distance(m=distance(delivery_pickup_location, user.current_location).meters) < closest_first[0]):
        #        closest_first = (Distance(m=distance(delivery_pickup_location, user.current_location).meters), user.user_id)
           

        nearest_delivery_person = delivery_persons_queryset.first()
        # print(closest_first)

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

@api_view(['POST'])
def assignedOrders(request):
    userId = jwt.decode(request.headers['token'], SECRET_KEY, algorithms=["HS256"])['id']
    deliveryUser= Delivery.objects.filter(id=userId['delivery_partner'])
    deliveries=[]
    for user in deliveryUser:
        deliveries.append({"delivery_id":user['id'],"order_id":user['order_id'],"pickup_address":user['pickup_address'],"delivery-address":user['delivery_address']})
    
    return Response(deliveries,status=status.HTTP_200_OK)