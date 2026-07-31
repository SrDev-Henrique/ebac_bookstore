# pyright: reportUnannotatedClassAttribute=false, reportExplicitAny=false, reportAny=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false

from __future__ import annotations

from typing import Any, override

from django.contrib.auth.models import User
from rest_framework import serializers

from order.models.order import Order
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer[Order]):
    product = ProductSerializer(read_only=True, many=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['product', 'total', 'user', 'products_id']
        extra_kwargs = {'product': {'required': False}}

    def get_total(self, instance: Order) -> int:
        return sum(product.price or 0 for product in instance.product.all())

    @override
    def create(self, validated_data: dict[str, Any]) -> Order:
        product_data: list[Product] = validated_data.pop('products_id')
        user_data: User = validated_data.pop('user')

        order = Order.objects.create(user=user_data, **validated_data)
        for product in product_data:
            order.product.add(product)
        return order

    @override
    def update(self, instance: Order, validated_data: dict[str, Any]) -> Order:
        products_data: list[Product] | None = validated_data.pop('products_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if products_data is not None:
            instance.product.set(products_data)
        return instance
