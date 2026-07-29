from django.db import IntegrityError
from django.test import TestCase

from product.models import Category, Product
from product.tests.factories import CategoryFactory, ProductFactory


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = CategoryFactory(
            title="Fiction",
            slug="fiction",
            description="Fiction books",
            active=True,
        )

        self.assertEqual(category.title, "Fiction")
        self.assertEqual(category.slug, "fiction")
        self.assertEqual(category.description, "Fiction books")
        self.assertTrue(category.active)

    def test_active_defaults_to_true(self):
        category = CategoryFactory()

        self.assertTrue(category.active)

    def test_slug_must_be_unique(self):
        CategoryFactory(slug="unique-slug")

        with self.assertRaises(IntegrityError):
            CategoryFactory(slug="unique-slug")

    def test_description_can_be_null(self):
        category = CategoryFactory(description=None)

        self.assertIsNone(category.description)


class ProductModelTest(TestCase):
    def test_create_product(self):
        product = ProductFactory(
            title="Django Book",
            description="Learn Django",
            price=5000,
            active=True,
        )

        self.assertEqual(product.title, "Django Book")
        self.assertEqual(product.description, "Learn Django")
        self.assertEqual(product.price, 5000)
        self.assertTrue(product.active)

    def test_active_defaults_to_true(self):
        product = ProductFactory()

        self.assertTrue(product.active)

    def test_product_can_have_categories(self):
        category = CategoryFactory()
        product = ProductFactory(category=[category])

        self.assertEqual(product.category.count(), 1)
        self.assertIn(category, product.category.all())

    def test_price_can_be_null(self):
        product = ProductFactory(price=None)

        self.assertIsNone(product.price)
