from rest_framework import serializers

from order.models.order import Order
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        return sum(product.price or 0 for product in instance.product.all())

    class Meta:
        model = Order
        fields = ['product', 'total']