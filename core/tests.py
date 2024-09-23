from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .serializers import NewCustomerSerializer, CustomerSerializer, OrderSerializer
from .models import Customer, Order


# Create your tests here.
class StoreTestCase(TestCase):
    def setUp(self):
        cutomer1 = {
            
        }