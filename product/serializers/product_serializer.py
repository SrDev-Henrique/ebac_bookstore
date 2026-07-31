# pyright: reportUnannotatedClassAttribute=false, reportExplicitAny=false, reportAny=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false

from __future__ import annotations

from typing import Any, override

from rest_framework import serializers

from product.models.category import Category
from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer[Product]):
    category = CategorySerializer(read_only=True, many=True)
    categories_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'active',
            'category',
            'categories_id',
        ]
        extra_kwargs = {'category': {'required': False}}

    @override
    def create(self, validated_data: dict[str, Any]) -> Product:
        categories_data: list[Category] = validated_data.pop('categories_id')
        product = Product.objects.create(**validated_data)
        for category in categories_data:
            product.category.add(category)
        return product

    @override
    def update(self, instance: Product, validated_data: dict[str, Any]) -> Product:
        categories_data: list[Category] | None = validated_data.pop('categories_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories_data is not None:
            instance.category.set(categories_data)
        return instance
