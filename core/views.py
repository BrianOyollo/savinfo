from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import CustomerSerializer, NewCustomerSerializer, OrderSerializer
from .permissions import IsAdminOrCustomer
from .models import Customer, Order
from .send_sms import send_order_confirmation_sms, send_order_update_sms

User = get_user_model()

# Create your views here.

class CustomersListCreateView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, format=None):
        serializer = NewCustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            customer_data = CustomerSerializer(customer).data 
            return Response(customer_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset = Customer.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

class CustomerDetailView(APIView):
    permission_classes = (IsAdminOrCustomer,)

    def get_customer(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        self.check_object_permissions(self.request, customer)
        return customer
        
    def get(self, request, pk, format=None):
        customer = self.get_customer(request, pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        customer = self.get_customer(request, pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_customer(request, pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrderListCreateView(APIView):
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # send order confirmation message
            customer = order.customer
            send_order_confirmation_sms(customer, order.item, order.quantity)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)