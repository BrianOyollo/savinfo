from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from .serializers import CustomerSerializer, NewCustomerSerializer, OrderSerializer
from .permissions import IsAdminOrCustomer, IsAdminOrOwnOrder
from .models import Customer, Order
from .send_sms import send_order_confirmation_sms, send_order_update_sms

User = get_user_model()

# Create your views here.

class CustomersListCreateView(APIView):
    permission_classes = (permissions.IsAdminUser,) # remove to allow self registration

    @swagger_auto_schema(operation_description = "Create a new customer", request_body=NewCustomerSerializer)
    def post(self, request, format=None):
        serializer = NewCustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            customer_data = CustomerSerializer(customer).data 
            return Response(customer_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_description = "List customers", responses={200: CustomerSerializer(many=True)})
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

    @swagger_auto_schema(operation_description = "Retrieve customer", responses={200: CustomerSerializer})   
    def get(self, request, pk, format=None):
        customer = self.get_customer(request, pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_description = "Update customer details", request_body=CustomerSerializer)
    def patch(self, request, pk, format=None):
        customer = self.get_customer(request, pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description = "Delete customer")
    def delete(self, request, pk, format=None):
        customer = self.get_customer(request, pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrdersListCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(operation_description = "Create a new order", request_body=OrderSerializer)
    def post(self, request, format=None):
        
        # admins can place orders for customers. A customer can only place their orders. 
        if request.user.is_superuser or int(request.data['customer']) == request.user.customer.id:
            serializer = OrderSerializer(data=request.data) 
        else:
            return Response({'error': 'Only admins can place orders for other customers'}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            order = serializer.save()

            # send order confirmation message
            # you can always force a customer to provide a phone_number before placing an order
            customer = order.customer
            if customer.phone_number:
                send_order_confirmation_sms(customer, order.item, order.quantity)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_description = "List orders", responses={200: OrderSerializer(many=True)})  
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
    
    @swagger_auto_schema(operation_description = "Retrieve order", responses={200: OrderSerializer})
    def get(self, request, pk, format=None):
        order = self.get_order(request, pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_description = "Update order", request_body=OrderSerializer)
    def patch(self, request, pk, format=None):
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
    
    @swagger_auto_schema(operation_description = "Delete order")
    def delete(self, request, pk, format=None):
        order = self.get_order(request, pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)