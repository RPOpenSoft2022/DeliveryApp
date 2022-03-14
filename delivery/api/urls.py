from django.urls import path
from .views import delivery_list
from api import views
from rest_framework.routers import DefaultRouter
app_name = 'api'


router= DefaultRouter()
router.register(r'delivery',delivery_list,basename='delivery')
# urlpatterns = [
#     path('delivery/', views.delivery_list.as_view())
# ]
urlpatterns=router.urls