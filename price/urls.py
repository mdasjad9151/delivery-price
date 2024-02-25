from django.urls import path
from . import views

urlpatterns = [
    path('price/', views.calculate_delivery_price, name='calculate_delivery_price'),
]