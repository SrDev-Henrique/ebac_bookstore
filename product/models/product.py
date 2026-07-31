#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from django.db import models

from .category import Category


class Product(models.Model):
    title: models.CharField[str, str] = models.CharField(max_length=100)
    description: models.TextField[str | None, str | None] = models.TextField(
        max_length=500, blank=True, null=True
    )
    price: models.PositiveIntegerField[int | None, int | None] = models.PositiveIntegerField(
        null=True
    )
    active: models.BooleanField[bool, bool] = models.BooleanField(default=True)
    category: models.ManyToManyField[Category, Category] = models.ManyToManyField(
        Category, blank=True
    )

    class Meta:
        ordering: list[str] = ['pk']
