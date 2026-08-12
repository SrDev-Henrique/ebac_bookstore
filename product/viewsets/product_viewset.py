from collections.abc import Sequence

from django.db.models import QuerySet
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.viewsets import ModelViewSet

from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet[Product]):
    permission_classes: Sequence[type[BasePermission]] = [AllowAny]
    serializer_class: type[ProductSerializer] = ProductSerializer
    queryset: QuerySet[Product] = Product.objects.all()
