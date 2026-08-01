from django.test import TestCase

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer
from product.tests.factories import CategoryFactory, ProductFactory


class CategorySerializerTest(TestCase):
    def test_serializer_accepts_valid_data(self):
        data = {
            'title': 'Fiction',
            'slug': 'fiction',
            'description': 'Fiction books',
            'active': True,
        }

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_requires_title(self):
        data = {
            'slug': 'fiction',
            'description': 'Fiction books',
            'active': True,
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_serializer_requires_slug(self):
        data = {
            'title': 'Fiction',
            'description': 'Fiction books',
            'active': True,
        }

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('slug', serializer.errors)

    def test_serializer_creates_category(self):
        data = {
            'title': 'Science',
            'slug': 'science',
            'description': 'Science books',
            'active': True,
        }

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.title, 'Science')
        self.assertEqual(category.slug, 'science')
        self.assertTrue(category.active)

    def test_serializer_returns_expected_fields(self):
        category = CategoryFactory(
            title='Fiction',
            slug='fiction',
            description='Fiction books',
            active=True,
        )

        serializer = CategorySerializer(category)

        expected_fields = {'title', 'slug', 'description', 'active'}

        self.assertEqual(set(serializer.data.keys()), expected_fields)


class ProductSerializerTest(TestCase):
    def test_serializer_accepts_valid_data(self):
        category = CategoryFactory()

        data = {
            'title': 'Django Book',
            'description': 'Learn Django',
            'price': 5000,
            'active': True,
            'categories_id': [category.id],
        }

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_requires_title(self):
        category = CategoryFactory()

        data = {
            'description': 'Learn Django',
            'price': 5000,
            'active': True,
            'categories_id': [category.id],
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_serializer_requires_category(self):
        data = {
            'title': 'Django Book',
            'description': 'Learn Django',
            'price': 5000,
            'active': True,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('categories_id', serializer.errors)

    def test_serializer_creates_product(self):
        category = CategoryFactory(
            title='Programming',
            slug='programming',
            description='Programming books',
            active=True,
        )

        data = {
            'title': 'Python Book',
            'description': 'Learn Python',
            'price': 3000,
            'active': True,
            'categories_id': [category.id],
        }

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.title, 'Python Book')
        self.assertEqual(product.price, 3000)
        self.assertEqual(product.category.count(), 1)

    def test_serializer_returns_expected_fields(self):
        product = ProductFactory()

        serializer = ProductSerializer(product)

        expected_fields = {'title', 'description', 'price', 'active', 'category'}

        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_serializer_represents_category_relationship(self):
        category = CategoryFactory(
            title='Fiction',
            slug='fiction',
            description='Fiction books',
            active=True,
        )
        product = ProductFactory(category=[category])

        serializer = ProductSerializer(product)
        category_data = serializer.data['category'][0]

        self.assertEqual(len(serializer.data['category']), 1)
        self.assertEqual(category_data['title'], 'Fiction')
        self.assertEqual(category_data['slug'], 'fiction')
        self.assertEqual(category_data['description'], 'Fiction books')
        self.assertTrue(category_data['active'])
