# pyright: reportUnannotatedClassAttribute=false, reportPrivateImportUsage=false, reportUnknownMemberType=false

import factory

from product.models.category import Category
from product.models.product import Product


class CategoryFactory(factory.django.DjangoModelFactory[Category]):
    class Meta:
        model = Category

    title = factory.Faker("pystr")
    slug = factory.Faker("pystr")
    description = factory.Faker("pystr")
    active = factory.Iterator([True, False])


class ProductFactory(factory.django.DjangoModelFactory[Product]):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    price = factory.Faker("pyint")
    title = factory.Faker("pystr")

    @factory.post_generation
    def category(
        self,
        create: bool,
        extracted: list[Category] | None,
    ) -> None:
        if not create:
            return
        if extracted:
            for item in extracted:
                self.category.add(item)  # pyright: ignore[reportAttributeAccessIssue]
