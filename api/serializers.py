import uuid
from rest_framework import serializers
from .models import Product,Order,OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock'
        ) # type: ignore

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price')

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        )
    
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self,obj):
        orders = obj.items.all()
        return sum(order.item_subtotal for order in orders)

    class Meta:
        model = Order
        fields = (
            'user',
            'order_id' ,
            'order_status' ,
            'items' ,
            'created_at' ,
            'total_price'
        )
