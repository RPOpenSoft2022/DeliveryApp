from django.urls import path
from .views import delivery_list
from api import views
app_name = 'api'

urlpatterns = [
    path('delivery/', views.delivery_list.as_view())
]
