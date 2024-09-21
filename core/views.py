from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import CustomerSerializer, NewCustomerSerializer, OrderSerializer
from .permissions import IsAdminOrCustomer, IsAdminOrOwnOrder
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
    

class OrdersListCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # send order confirmation message
            # you can always force a customer to provide a phone_number before placing an order
            customer = order.customer
            if customer.phone_number:
                send_order_confirmation_sms(customer, order.item, order.quantity)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        if request.user.is_superuser:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(customer__user = request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    permission_classes = (IsAdminOrOwnOrder,)
    def get_order(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(self.request, order)
        return order
    
    def get(self, request, pk, format=None):
        order = self.get_order(request, pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        order = self.get_order(request, pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            updated_order = serializer.save()

            # send order update message
            customer = updated_order.customer
            if customer.phone_number: 
                send_order_update_sms(customer, updated_order.item, updated_order.quantity)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        order = self.get_order(request, pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)