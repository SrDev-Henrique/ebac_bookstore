from collections.abc import Sequence

from django.db.models import QuerySet
from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from product.models import Category
from product.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet[Category]):
    authentication_classes: Sequence[type[BaseAuthentication]] = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes: Sequence[type[BasePermission]] = [IsAuthenticated]
    serializer_class: type[CategorySerializer] = CategorySerializer
    queryset: QuerySet[Category] = Category.objects.all()
