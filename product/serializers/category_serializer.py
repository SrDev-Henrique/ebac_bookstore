# pyright: reportUnannotatedClassAttribute=false, reportExplicitAny=false, reportAny=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false

from __future__ import annotations

from rest_framework import serializers

from product.models.category import Category


class CategorySerializer(serializers.ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'description',
            'active',
        ]
