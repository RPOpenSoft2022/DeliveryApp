from django.urls import path
from .views import delivery_list
app_name = 'api'

urlpatterns = [
    path('delivery/', delivery_list)
]
