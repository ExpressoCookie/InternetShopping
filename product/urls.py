from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemList.as_view()),
    path('<int:pk>/', views.ItemDetail.as_view()),
    path('category/<str:slug>', views.category_page),
    path('manufacturer/<str:slug>', views.manufacturer_page),
    path('create_product', views.ItemCreate.as_view()),
    path('update_product/<int:pk>/', views.ItemUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('search/<str:q>/', views.ItemSearch.as_view()),
]