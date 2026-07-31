from django.test import TestCase

from order.serializers import OrderSerializer
from order.tests.factories import OrderFactory
from product.tests.factories import CategoryFactory, ProductFactory


class OrderSerializerTest(TestCase):
    def test_serializer_returns_expected_fields(self):
        order = OrderFactory()

        serializer = OrderSerializer(order)

        expected_fields = {'product', 'total'}

        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_serializer_calculates_total(self):
        products = ProductFactory.create_batch(2, price=1000)
        order = OrderFactory(product=products)

        serializer = OrderSerializer(order)

        self.assertEqual(serializer.data['total'], 2000)

    def test_serializer_represents_product_with_category(self):
        category = CategoryFactory(
            title='Fiction',
            slug='fiction',
            description='Fiction books',
            active=True,
        )
        product = ProductFactory(
            title='Django Book',
            price=5000,
            category=[category],
        )
        order = OrderFactory(product=[product])

        serializer = OrderSerializer(order)
        product_data = serializer.data['product'][0]
        category_data = product_data['category'][0]

        self.assertEqual(len(serializer.data['product']), 1)
        self.assertEqual(product_data['title'], 'Django Book')
        self.assertEqual(product_data['price'], 5000)
        self.assertEqual(category_data['title'], 'Fiction')
        self.assertEqual(category_data['slug'], 'fiction')

    def test_serializer_requires_product(self):
        data = {}

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product', serializer.errors)

    def test_serializer_accepts_valid_data(self):
        data = {
            'product': [
                {
                    'title': 'Django Book',
                    'description': 'Learn Django',
                    'price': 5000,
                    'active': True,
                    'category': [
                        {
                            'title': 'Technology',
                            'slug': 'technology',
                            'description': 'Tech books',
                            'active': True,
                        }
                    ],
                }
            ],
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
