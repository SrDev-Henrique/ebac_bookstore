from collections.abc import Sequence

from django.db.models import QuerySet
from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet[Order]):
    authentication_classes: Sequence[type[BaseAuthentication]] = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes: Sequence[type[BasePermission]] = [IsAuthenticated]
    serializer_class: type[OrderSerializer] = OrderSerializer
    queryset: QuerySet[Order] = Order.objects.all()
