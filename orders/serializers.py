from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import UserSerializer
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
