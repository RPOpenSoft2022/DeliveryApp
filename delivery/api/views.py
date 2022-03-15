from api.serializers import DeliverySerializer, DeliveryUserSerializer
from rest_framework.decorators import api_view
from . models import Delivery,DeliveryUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets

# Create your views here.
# @api_view(['GET', 'POST'])
# def delivery_list(request):
#     """
#     List all delivery/ Create One Delivery
#     """
#     if request.method == 'GET':
#         delivery_objects = Delivery.objects.all()
#         serializer = DeliverySerializer(delivery_objects, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = DeliverySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class delivery_list(APIView):
#     def get(self,request):
#         delivery_objects = Delivery.objects.all()
#         serializer = DeliverySerializer(delivery_objects, many=True)
#         return Response(serializer.data)

#     def post(self,request):
#         serializer = DeliverySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryViewsets(viewsets.ModelViewSet):
    queryset=Delivery.objects.all()
    serializer_class=DeliverySerializer
    permission_classes=[]


class DeliveryUserViewsets(viewsets.ModelViewSet):
    queryset=DeliveryUser.objects.all()
    serializer_class=DeliveryUserSerializer
    permission_classes=[]