# pyright: reportUnannotatedClassAttribute=false, reportExplicitAny=false, reportAny=false

from __future__ import annotations

from typing import Any, override

from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    @override
    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)
