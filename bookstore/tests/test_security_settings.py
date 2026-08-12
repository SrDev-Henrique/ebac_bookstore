# pyright: reportUnannotatedClassAttribute=false, reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportAny=false

from typing import override

from django.conf import settings
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.factories import CategoryFactory, ProductFactory


class SecuritySettingsTest(SimpleTestCase):
    def test_authentication_classes_are_configured(self):
        # Guards against typos such as DETAIL_AUTHENTICATION_CLASSES, which
        # DRF silently ignores, leaving every endpoint without authentication.
        self.assertIn('DEFAULT_AUTHENTICATION_CLASSES', settings.REST_FRAMEWORK)

    def test_expected_authentication_backends_are_enabled(self):
        configured = settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']

        self.assertIn(
            'rest_framework.authentication.TokenAuthentication', configured
        )
        self.assertIn(
            'rest_framework.authentication.SessionAuthentication', configured
        )

    def test_security_middleware_is_enabled(self):
        for middleware in (
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ):
            with self.subTest(middleware=middleware):
                self.assertIn(middleware, settings.MIDDLEWARE)

    def test_password_validators_are_enabled(self):
        validators = {
            validator['NAME'] for validator in settings.AUTH_PASSWORD_VALIDATORS
        }

        self.assertIn(
            'django.contrib.auth.password_validation.MinimumLengthValidator',
            validators,
        )
        self.assertIn(
            'django.contrib.auth.password_validation.CommonPasswordValidator',
            validators,
        )

    def test_pagination_limits_response_size(self):
        # An unbounded list endpoint is a denial-of-service vector.
        self.assertIn('DEFAULT_PAGINATION_CLASS', settings.REST_FRAMEWORK)
        self.assertLessEqual(settings.REST_FRAMEWORK['PAGE_SIZE'], 100)

    def test_default_permission_allows_anonymous(self):
        configured = settings.REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']

        self.assertIn('rest_framework.permissions.AllowAny', configured)


class CsrfProtectionTest(APITestCase):
    client: APIClient
    user: User
    password: str
    url: str

    @override
    def setUp(self) -> None:
        self.client = APIClient(enforce_csrf_checks=True)
        self.password = 'a-very-secret-password'
        self.user = User.objects.create_user(
            username='csrf-user',
            email='csrf@example.com',
            password=self.password,
        )
        self.url = '/bookstore/v1/products/'

    def test_session_authenticated_write_without_csrf_token_is_blocked(self):
        _ = self.client.login(username=self.user.username, password=self.password)
        categories = CategoryFactory.create_batch(1)
        payload = {
            'title': 'CSRF Book',
            'description': 'Should be blocked',
            'price': 100,
            'active': True,
            'categories_id': [category.pk for category in categories],
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_session_authenticated_read_is_allowed(self):
        _ = self.client.login(username=self.user.username, password=self.password)
        _ = ProductFactory(category=CategoryFactory.create_batch(1))

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ClickjackingHeaderTest(APITestCase):
    def test_responses_carry_x_frame_options(self):
        response = self.client.get('/bookstore/v1/categories/')

        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
