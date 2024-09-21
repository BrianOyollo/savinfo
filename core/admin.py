from django.contrib import admin
from .models import Customer, Order

class CustomCustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('id','code', 'name', 'phone_number', )

class CustomOrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('item', 'quantity', 'created_at', 'customer', )


# Register your models here.
admin.site.register(Customer, CustomCustomerAdmin)
admin.site.register(Order, CustomOrderAdmin)
