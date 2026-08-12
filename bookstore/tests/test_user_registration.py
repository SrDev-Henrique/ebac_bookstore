# pyright: reportUnannotatedClassAttribute=false, reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportAny=false

from typing import override

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class UserRegistrationTest(APITestCase):
    client: APIClient
    url: str

    @override
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = '/bookstore/v1/users/'

    def test_anonymous_can_register(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'a-very-secret-password',
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['email'], 'newuser@example.com')
        self.assertNotIn('password', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertTrue(user.check_password('a-very-secret-password'))

    def test_duplicate_username_is_rejected(self):
        _ = User.objects.create_user(
            username='taken',
            email='taken@example.com',
            password='a-very-secret-password',
        )
        payload = {
            'username': 'taken',
            'email': 'other@example.com',
            'password': 'a-very-secret-password',
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username='taken').count(), 1)

    def test_password_is_required(self):
        payload = {
            'username': 'nopass',
            'email': 'nopass@example.com',
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username='nopass').exists())

    def test_list_users_is_not_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
