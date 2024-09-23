import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_create_superuser():
    superuser = User.objects.create_superuser(
        username = 'superuser',
        email = 'superuser@example.com',
        password = 'SuperPassword',
    )
    assert superuser.username =='superuser'
    assert superuser.email =='superuser@example.com'
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.is_active

def test_create_user():
    user = User.objects.create_user(
        username = 'testuser',
        email = 'testuser@example.com',
        password = 'TestPassword',
    )
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.is_active
    assert not user.is_superuser

def test_create_user_without_username():
    with pytest.raises(TypeError):
        User.objects.create_user(
            email = 'testuser@example.com',
            password = 'TestPassword',
        )
        
def test_create_user_without_email():
    with pytest.raises(TypeError):
        User.objects.create_user(
            username = 'testuser',
            password = 'TestPassword',
        )


