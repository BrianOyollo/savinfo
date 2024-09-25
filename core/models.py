from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator 
from django.core.exceptions import ValidationError

User = get_user_model()

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=13, validators=[MinValueValidator(10)],  null=True, blank=True)
    code = models.CharField(max_length=8, null = False, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    item = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)] ,null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'{self.item} - {self.customer}'
    
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than 0')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)