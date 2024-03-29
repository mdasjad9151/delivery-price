from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('price/', views.calculate_delivery_price, name='calculate_delivery_price'),

    path('create/organization/', views.create_organization, name='create_organization'),
    path('create/item/', views.create_item, name='create_item'),
    path('create/pricing/', views.create_pricing, name='create_pricing'),

]