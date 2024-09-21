from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Customer
from .utils import generate_unique_code

User = get_user_model()

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        user = instance
        name = instance.username
        code  = generate_unique_code()

        Customer.objects.create(user=user, name=name, code=code)