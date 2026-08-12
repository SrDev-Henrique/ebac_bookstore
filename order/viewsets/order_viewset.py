from collections.abc import Sequence

from django.db.models import QuerySet
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet[Order]):
    permission_classes: Sequence[type[BasePermission]] = [AllowAny]
    serializer_class: type[OrderSerializer] = OrderSerializer
    queryset: QuerySet[Order] = Order.objects.all()
