from collections.abc import Sequence

from django.db.models import QuerySet
from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet[Product]):
    authentication_classes: Sequence[type[BaseAuthentication]] = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes: Sequence[type[BasePermission]] = [IsAuthenticated]
    serializer_class: type[ProductSerializer] = ProductSerializer
    queryset: QuerySet[Product] = Product.objects.all()