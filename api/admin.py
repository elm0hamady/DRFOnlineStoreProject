from django.contrib import admin
from .models import OrderItem ,Order,User
class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
admin.site.register(User)