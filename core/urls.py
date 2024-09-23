from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('customers/', views.CustomersListCreateView.as_view(), name='customers-list-create'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name ='customer-details'),
    path('orders/', views.OrdersListCreateView.as_view(), name='orders-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-details'),
]