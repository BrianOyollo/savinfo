from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_superuser', 'is_staff', 'is_active',)

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)