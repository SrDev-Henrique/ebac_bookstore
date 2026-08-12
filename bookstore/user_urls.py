from django.urls import path, include
from rest_framework import routers

from bookstore import viewsets

router = routers.SimpleRouter()
router.register(r'users', viewsets.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
