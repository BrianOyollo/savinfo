from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError

import pytest
from ..models import Customer, Order

User = get_user_model()
# pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestCustomerEndpoints:

    @pytest.mark.parametrize('user_role, expected_status',[
        ('authenticated_superuser', 201),
        ('api_client', 401), # api_client has no authenication
    ])
    def test_create_customer(self, user_role, expected_status, request):
        payload = {
            'email':'testuser1@example.com',
            'username':'testuser1',
            'phone_number':'0712345678',
            'password':'TestPassword1'
        }

        client = request.getfixturevalue(user_role)
        response = client.post('/api/customers/', data=payload, format='json')

        assert response.status_code == expected_status
        if response.status_code == 201:
            assert response.data['name'] == payload['username']
            assert response.data['phone_number'] == payload['phone_number']
            assert response.data['code'] != None


    @pytest.mark.parametrize('user_role, expected_status',[
        ('authenticated_superuser', 200),
        ('api_client', 401),
    ])
    def test_list_customers(self, user_role, expected_status, request):
        payload = {
            'email':'testuser1@example.com',
            'username':'testuser1',
            'phone_number':'0712345678',
            'password':'TestPassword1'
        }

        client = request.getfixturevalue(user_role)
        client.post('/api/customers/', data=payload, format='json')

        response = client.get('/api/customers/', format='json')
        assert response.status_code == expected_status
        if response.status_code == 200:
            assert len(response.data) > 0 # atleast one customer is returned


    def test_create_customer_missing_fields(self, authenticated_superuser):
        payload = {
            'email': 'testuser2@example.com',
            # 'username' is missing
            'phone_number':'0712345678',
            'password': 'TestPassword2'
        }
        response = authenticated_superuser.post('/api/customers/', data=payload, format='json')
        assert response.status_code == 400

    def test_create_customer_existing_email(self, authenticated_superuser):
        payload = {
            'email': 'testuser3@example.com',
            'username': 'testuser3',
            'phone_number':'0712345678',
            'password': 'TestPassword3'
        }
        # create the customer
        authenticated_superuser.post('/api/customers/', data=payload, format='json')

        # create the same customer again
        response = authenticated_superuser.post('/api/customers/', data=payload, format='json')
        assert response.status_code == 400


    @pytest.mark.parametrize('user_role, expected_status',[
        ('authenticated_superuser', 200),
        ('api_client', 401),
    ])
    def test_retrieve_customer(self, user_role, expected_status, request ):
        payload = {
            'email': 'testuser4@example.com',
            'username': 'testuser4',
            'phone_number':'0712345678',
            'password': 'TestPassword4'
        }

        client = request.getfixturevalue(user_role)
        response = client.post('/api/customers/', data=payload, format='json')

        if response.status_code == 201:
            customer_id = response.data['id']
            customer_code = response.data['code']

            # retrieve the customer
            response = client.get(f'/api/customers/{customer_id}/', format='json')

            assert response.status_code == expected_status
            assert response.data['name'] == payload['username']
            assert response.data['code'] == customer_code

        else:
            assert response.status_code == expected_status


    @pytest.mark.parametrize('user_role, expected_status',[
        ('authenticated_superuser', 200),
        ('api_client', 401),
    ])
    def test_update_customer(self, user_role, expected_status, request):
        # Create a customer
        payload = {
            'email': 'testuser5@example.com',
            'username': 'testuser5',
            'phone_number':'0712345678',
            'password': 'TestPassword5'
        }

        client = request.getfixturevalue(user_role)
        response = client.post('/api/customers/', data=payload, format='json')

        if response.status_code == 201:
            customer_id = response.data['id']

            # Update the customer's details
            update_payload = {
                'name': 'TestUser5',
                'phone_number':'0722345678',
            }
            response = client.patch(f'/api/customers/{customer_id}/', data=update_payload, format='json')
            assert response.status_code == expected_status
            assert response.data['name'] == update_payload['name']
            assert response.data['phone_number'] == update_payload['phone_number']

        else:
            assert response.status_code == expected_status

    
    @pytest.mark.parametrize('user_role, expected_status', [
        ('authenticated_superuser', 204), 
        ('api_client', 401),
    ])
    def test_delete_customer(self, user_role, expected_status, request):
        # Create a customer
        payload = {
            'email': 'testuser6@example.com',
            'username': 'testuser6',
            'phone_number':'0712345678',
            'password': 'TestPassword6'
        }

        client = request.getfixturevalue(user_role)
        response = client.post('/api/customers/', data=payload, format='json')

        if response.status_code == 201:
            customer_id = response.data['id']

            # Delete the customer
            response = client.delete(f'/api/customers/{customer_id}/')
            
            assert response.status_code == expected_status

            # Optionally, check if the customer was actually deleted
            if expected_status == expected_status:
                assert client.get(f'/api/customers/{customer_id}/').status_code == 404  # confirm customer nolonger exists
        else:
            assert response.status_code == expected_status



@pytest.mark.django_db
class TestOrderEndpoints:

    @pytest.mark.parametrize('user_role, expected_status', [
        ('authenticated_superuser', 201), # authenticated admins can create orders for customers
        ('api_client', 401), # unautheticated users can't create orders
    ])
    def test_create_order_admin(self, create_user, user_role, expected_status, mock_send_sms, request):
        # create a customer
        customer = create_user.customer

        payload = {
            'item':'2000 Toyota Land Cruiser',
            'quantity':1,
            'customer':customer.id
        }

        client = request.getfixturevalue(user_role)
        response = client.post('/api/orders/', data=payload, format='json')
        assert response.status_code == expected_status
        if response.status_code == 201:
            assert response.data['item'] == payload['item']
            assert response.data['quantity'] == payload['quantity']
            assert response.data['status'] == 'pending'
            assert response.data['customer'] == customer.id
            assert response.data['customer_code'] == customer.code


    def test_create_order_authenicated_user(self, create_user, mock_send_sms, api_client):
        user = create_user
        print(f'user:{user}')
        customer = user.customer
        print(f'customer:{customer.user}-{customer} - {customer.id}')
        api_client.force_authenticate(user=user)

        payload = {
            'item':'2000 Toyota Land Cruiser',
            'quantity':1,
            'customer':customer.id
        }

        response = api_client.post('/api/orders/', data=payload, format='json')
        assert response.status_code == 201
        assert response.data['item'] == payload['item']
        assert response.data['quantity'] == payload['quantity']
        assert response.data['status'] == 'pending'
        assert response.data['customer'] == customer.id
        assert response.data['customer_code'] == customer.code

    def test_create_order_authenicated_user_different_customer(self, create_user, authenticated_user):
        payload = {
            'item':'2000 Toyota Land Cruiser',
            'quantity':1,
            'customer':42
        }

        response = authenticated_user.post('/api/orders/', data=payload, format='json')
        assert response.status_code == 403

    def test_create_order_invalid_quantity(self, create_user, authenticated_superuser):
        customer = create_user.customer
        payload = {
            'item':'2000 Toyota Land Cruiser',
            'quantity':0,
            'customer':customer.id
        }

        response = authenticated_superuser.post('/api/orders/', data=payload, format='json')
        assert response.status_code == 400

    def test_create_order_missing_item(self, create_user,  authenticated_superuser):
        customer = create_user.customer
        payload = {
            # 'item':'2000 Toyota Land Cruiser',
            'quantity':0,
            'customer':customer.id
        }

        response = authenticated_superuser.post('/api/orders/', data=payload, format='json')
        assert response.status_code == 400
    
    def test_create_order_missing_customer(self, authenticated_superuser):
        # customer = create_user.customer
        payload = {
            'item':'2000 Toyota Land Cruiser',
            'quantity':0,
            # 'customer':customer.id
        }

        response = authenticated_superuser.post('/api/orders/', data=payload, format='json')
        assert response.status_code == 400
        
    
    @pytest.mark.parametrize('user_role, expected_status', [
        ('authenticated_superuser', 200), # authenticated admins can create orders for customers
        ('api_client', 401), # unautheticated users retrieve an order
    ])
    def test_retrieve_order_admin(self, create_order, user_role, expected_status, request):
        order = create_order

        client = request.getfixturevalue(user_role)
        response = client.get(f'/api/orders/{order.id}/', format='json')

        assert response.status_code == expected_status
        if response.status_code == 200:
            assert response.data['item'] == order.item
            assert response.data['quantity'] == order.quantity
            assert response.data['status'] == order.status
            assert response.data['customer'] == order.customer.id
            assert response.data['customer_code'] == order.customer.code

    
    def test_retrieve_order_customer_order(self, create_order, api_client):
        order = create_order
        user = order.customer.user

        api_client.force_authenticate(user=user)
        response = api_client.get(f'/api/orders/{order.id}/', format='json')

        assert response.status_code == 200
        assert response.data['item'] == order.item
        assert response.data['quantity'] == order.quantity
        assert response.data['status'] == order.status
        assert response.data['customer'] == order.customer.id
        assert response.data['customer_code'] == order.customer.code

    def test_retrieve_order_different_customer_order(self, create_order, authenticated_user):
        order = create_order
        response = authenticated_user.get(f'/api/orders/{order.id}/', format='json')
        assert response.status_code == 403

    def test_update_order_admin(self, create_order, mock_send_sms, authenticated_superuser):
        order = create_order
        payload = {
            'quantity':2,
           'status':'completed'
        }

        response = authenticated_superuser.patch(f'/api/orders/{order.id}/', data=payload, format='json')

        assert response.status_code == 200
        assert response.data['quantity'] == payload['quantity']
        assert response.data['status'] == payload['status']

    
    def test_update_customer_own_order(self, create_order, mock_send_sms,  api_client):
        order = create_order
        payload = {
            'quantity':2,
           'status':'completed'
        }
        api_client.force_authenticate(user=order.customer.user)
        response = api_client.patch(f'/api/orders/{order.id}/', data=payload, format='json')

        assert response.status_code == 200
        assert response.data['quantity'] == payload['quantity']
        assert response.data['status'] == payload['status']

    def test_update_different_customer_order(self, create_order, authenticated_user):
        order = create_order
        payload = {
            'quantity':2,
           'status':'completed'
        }
        response = authenticated_user.patch(f'/api/orders/{order.id}/', data=payload, format='json')

        assert response.status_code == 403



        