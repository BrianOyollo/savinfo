from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import pytest
from ..models import Customer, Order

User = get_user_model()
pytestmark = pytest.mark.django_db

class TestCustomerModel:
    def test_create_customer_when_user_is_created(self, create_user):
        customer = Customer.objects.get(user=create_user)

        assert customer.user == create_user
        assert customer.name == create_user.username
        assert customer.phone_number == None
        assert customer.code != None
        

    def test_create_customer_without_user(self):
        with pytest.raises(IntegrityError):
            Customer.objects.create(
                name = 'testuser',
                phone_number = '1234567890',
                code = '123456',
            )
    def test_create_customer_with_noexisting_user(self):
        with pytest.raises(User.DoesNotExist):
            Customer.objects.create(
                user = User.objects.get(email='nonexistentuser@example.com'),
                name = 'testuser',
                phone_number = '1234567890',
                code = '123456',
            )
    
    def test_update_customer(self, create_user):
        new_name = 'Test User'
        phone_number = '1234567890'

        customer = Customer.objects.get(user = create_user)
        customer.name =new_name
        customer.phone_number = phone_number
        customer.save()

        updated_customer = Customer.objects.get(user=create_user)
        assert updated_customer.name == new_name
        assert updated_customer.phone_number == phone_number


class TestOrderModel:

    def test_create_order(self, create_user):
        customer = create_user.customer
        order = Order.objects.create(
            item = '2006 Ford F-250 Super Duty Lariat',
            quantity = 1,
            customer = customer
        )

        assert order.item == '2006 Ford F-250 Super Duty Lariat'
        assert order.quantity == 1
        assert order.customer.user == create_user

    def test_order_default_status(self, create_user):
        customer = create_user.customer
        order = Order.objects.create(
            item='2006 Ford F-250 Super Duty Lariat',
            quantity=1,
            customer=customer
        )
        assert order.status == 'pending'

    def test_order_quantity_validation(self, create_user):
        customer = create_user.customer
        with pytest.raises(ValidationError): 
            Order.objects.create(
                item='2006 Ford F-250 Super Duty Lariat',
                quantity=0, # quantity must be > 0
                customer=customer
            )
