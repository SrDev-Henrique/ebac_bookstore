import factory

from product.models import Product, Category

class CategoryFactory(factory.django.DjangoModelFactory[Category]):
    title = factory.Faker("pystr")
    slug = factory.Faker("pystr")
    description = factory.Faker("pystr")
    active = factory.Iterator([True, False])

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory[Product]):
    price = factory.Faker("pyint")
    title = factory.Faker("pystr")

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.category.add(item)  # pyright: ignore[reportAttributeAccessIssue]

    class Meta:
        model = Product
            