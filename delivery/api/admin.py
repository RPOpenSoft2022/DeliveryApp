from ast import Del
from django.contrib import admin

# Register your models here.
from . models import Delivery, DeliveryUser

admin.site.register(Delivery)
admin.site.register(DeliveryUser)