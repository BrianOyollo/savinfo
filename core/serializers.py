from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Customer, Order
from .utils import generate_unique_code

User = get_user_model()

class NewCustomerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
    email = serializers.EmailField(allow_blank=False, allow_null=False)
    phone_number = serializers.CharField(max_length=15, allow_blank=False, allow_null=False)
    password = serializers.CharField(min_length=12, write_only=True)

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')

        # Create User and Customer
        with transaction.atomic():
            user = User.objects.create_user(username=username, email=email, password=password)
            code = generate_unique_code()
            customer = Customer.objects.create(user=user, phone_number=phone_number, code=code, name=username)

        return customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'phone_number', 'code', 'created_at', 'user')
        read_only_fields = ('id','user', 'code')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'item', 'quantity','status', 'created_at', 'customer')
        read_only_fields = ('id',)









    

