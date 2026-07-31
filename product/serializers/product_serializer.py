from rest_framework import serializers

from product.models import Category, Product
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        categories_data = validated_data.pop('categories_id')
        product = Product.objects.create(**validated_data)
        for category in categories_data:
            product.category.add(category)
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories_data is not None:
            instance.category.set(categories_data)
        return instance
