from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('customers/', views.CustomersListCreateView.as_view()),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view()),
    path('orders/', views.OrdersListCreateView.as_view()),
    path('orders/<int:pk>/', views.OrderDetailView.as_view()),
]