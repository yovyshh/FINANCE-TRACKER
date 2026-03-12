from django.contrib import admin
from .models import Register

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'contact']  # Fields to display in the admin list view
    search_fields = ['username', 'email']           # Fields to search by in the admin
