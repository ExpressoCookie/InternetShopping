from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('my_page/', views.my_page),
    path('manufacturer_page/', views.manufacturer_page)
]
