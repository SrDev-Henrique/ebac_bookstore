from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet

from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet[Product]):
    serializer_class: type[ProductSerializer] = ProductSerializer
    queryset: QuerySet[Product] = Product.objects.all()