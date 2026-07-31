from django.urls import path, include
from rest_framework import routers

from product import viewsets

router = routers.SimpleRouter()
router.register(r'categories', viewsets.CategoryViewSet, basename='category')
router.register(r'products', viewsets.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
