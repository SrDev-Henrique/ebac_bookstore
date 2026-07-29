import factory

from product.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory[Category]):
    class Meta:
        model = Category

    title = factory.Faker("word")
    slug = factory.Sequence(lambda n: f"category-{n}")
    description = factory.Faker("sentence")
    active = True


class ProductFactory(factory.django.DjangoModelFactory[Product]):
    class Meta:
        model = Product

    title = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=500)
    price = factory.Faker("random_int", min=1, max=10000)
    active = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.category.add(item)  # pyright: ignore[reportAttributeAccessIssue]
