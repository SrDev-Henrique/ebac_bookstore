from rest_framework import serializers

from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'active',
            'category',
        ]

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        categories = [
            CategorySerializer().create(item)
            for item in category_data
        ]
        product = Product.objects.create(**validated_data)
        product.category.set(categories)
        return product

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if category_data is not None:
            categories = [
                CategorySerializer().create(item)
                for item in category_data
            ]
            instance.category.set(categories)

        return instance