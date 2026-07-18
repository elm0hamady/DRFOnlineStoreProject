import django_filters
from .models import Product , Order
from rest_framework import filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name" : ['iexact','icontains'],
            "price" : ['exact','gt','gte','lt','lte','range']
        }

class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
    
class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            "order_status" : ['iexact'],
            "created_at" : ['exact','gt','gte','lt','lte','range']
        }