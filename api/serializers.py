from django.db import transaction
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

class OrderCreateSerializer(serializers.ModelSerializer): 
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product','quantity')
    
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True,required=False)

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if items_data is not None:
                instance.items.all().delete()

                for item in items_data:
                    OrderItem.objects.create(order=instance,**item)
        return instance

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in items_data:
                OrderItem.objects.create(order=order,**item)
        return order
    
    class Meta:
        model = Order
        fields = (
            'user',
            'order_id' ,
            'order_status' ,
            'items'
        )
        extra_kwargs = {
            'user':{'read_only': True}
        }

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
