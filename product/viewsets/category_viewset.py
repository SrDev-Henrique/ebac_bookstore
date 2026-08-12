from collections.abc import Sequence

from django.db.models import QuerySet
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.viewsets import ModelViewSet

from product.models import Category
from product.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet[Category]):
    permission_classes: Sequence[type[BasePermission]] = [AllowAny]
    serializer_class: type[CategorySerializer] = CategorySerializer
    queryset: QuerySet[Category] = Category.objects.all()
