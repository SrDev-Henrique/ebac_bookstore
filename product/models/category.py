#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import override

from django.db import models


class Category(models.Model):
    title: models.CharField[str, str] = models.CharField(max_length=100)
    slug: models.SlugField[str, str] = models.SlugField(unique=True)
    description: models.CharField[str | None, str | None] = models.CharField(
        max_length=200, blank=True, null=True
    )
    active: models.BooleanField[bool, bool] = models.BooleanField(default=True)

    class Meta:
        ordering: list[str] = ['pk']

    @override
    def __str__(self) -> str:
        return self.title
