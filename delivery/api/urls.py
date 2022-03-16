from django.urls import path
from .views import DeliveryViewsets,DeliveryUserViewsets,getDeliveryOTP
from api import views
from rest_framework.routers import DefaultRouter
app_name = 'api'


router= DefaultRouter()
router.register(r'delivery',DeliveryViewsets,basename='delivery')
router.register(r'delivery_user',DeliveryUserViewsets,)
router.register(r'verifyotp',getDeliveryOTP)

urlpatterns=router.urls

# urlpatterns = [
#     path('delivery/', views.delivery_list.as_view())
# ]