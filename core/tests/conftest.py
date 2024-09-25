from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient
from unittest.mock import patch
import os
from ..models import Customer, Order

User = get_user_model()

@pytest.fixture
def api_client():
    yield APIClient()

@pytest.fixture
def create_user():
    user = User.objects.create_user(
        username = 'testuser',
        email = 'testuser@example.com',
        password = 'TestPassword',
    )
    return user

@pytest.fixture
def create_user2():
    user = User.objects.create_user(
        username = 'testuser2',
        email = 'testuser2@example.com',
        password = 'TestPassword',
    )
    return user

@pytest.fixture
def create_superuser():
    superuser = User.objects.create_superuser(
        username = 'superuser',
        email = 'superuser@example.com',
        password = 'SuperPassword',
    )
    return superuser

@pytest.fixture
def authenticated_superuser(create_superuser, api_client):
    api_client.force_authenticate(user=create_superuser)
    return api_client


@pytest.fixture
def authenticated_user(create_user, api_client):
    api_client.force_authenticate(user=create_user)
    return api_client
    
@pytest.fixture
def create_order(create_user2):
    customer = create_user2.customer
    order = Order.objects.create(item='2000 Toyota Land Cruiser', quantity=1, customer=customer)
    return order

@pytest.fixture
def mock_send_sms():
    with patch('core.send_sms.sms.send') as mock_send:
        mock_send.return_value = {
            "SMSMessageData": {
                "Message": "Sent to 1/1 Total Cost: KES 0.8000",
                "Recipients": [{
                    "statusCode": 101,
                    "number": "+254711XXXXXXX",
                    "status": "Success",
                    "cost": "KES 0.8000",
                    "messageId": "ATPid_SampleTxnId123"
                }]
            }
        }
        
        yield mock_send 