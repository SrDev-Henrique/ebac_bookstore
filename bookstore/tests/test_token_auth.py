# pyright: reportUnannotatedClassAttribute=false, reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportAny=false

from typing import override

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class TokenAuthEndpointTest(APITestCase):
    client: APIClient
    user: User
    username: str
    password: str
    url: str

    @override
    def setUp(self) -> None:
        self.client = APIClient()
        self.username = 'token-user'
        self.password = 'a-very-secret-password'
        self.user = User.objects.create_user(
            username=self.username,
            email='token@example.com',
            password=self.password,
        )
        self.url = '/api-token-auth/'

    def test_valid_credentials_return_token(self):
        response = self.client.post(
            self.url,
            {'username': self.username, 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['token'], Token.objects.get(user=self.user).key
        )

    def test_wrong_password_does_not_return_token(self):
        response = self.client.post(
            self.url,
            {'username': self.username, 'password': 'wrong'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_unknown_user_does_not_return_token(self):
        response = self.client.post(
            self.url,
            {'username': 'ghost', 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_inactive_user_cannot_obtain_token(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            self.url,
            {'username': self.username, 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_missing_credentials_are_rejected(self):
        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_is_not_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_response_does_not_leak_password(self):
        response = self.client.post(
            self.url,
            {'username': self.username, 'password': self.password},
            format='json',
        )

        self.assertNotIn(self.password.encode(), response.content)
