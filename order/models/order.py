from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models

from product.models.product import Product


class Order(models.Model):
    product: models.ManyToManyField[Product, Product] = models.ManyToManyField(
        Product, blank=False
    )
    user: models.ForeignKey[User, User] = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    class Meta:
        ordering: list[str] = ['pk']
