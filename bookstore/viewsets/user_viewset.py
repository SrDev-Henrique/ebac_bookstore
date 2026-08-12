from collections.abc import Sequence

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, BasePermission

from bookstore.serializers import UserRegistrationSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet[User]):
    permission_classes: Sequence[type[BasePermission]] = [AllowAny]
    serializer_class: type[UserRegistrationSerializer] = UserRegistrationSerializer
    queryset: QuerySet[User] = User.objects.all()
