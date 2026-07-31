# pyright: reportUnannotatedClassAttribute=false, reportPrivateImportUsage=false, reportUnknownMemberType=false

import factory

from product.models.category import Category
from product.models.product import Product


def _category_slug(n: int) -> str:
    return f"category-{n}"


class CategoryFactory(factory.django.DjangoModelFactory[Category]):
    class Meta:
        model = Category

    title = factory.Faker("word")
    slug = factory.Sequence(_category_slug)
    description = factory.Faker("sentence")
    active = True


class ProductFactory(factory.django.DjangoModelFactory[Product]):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    title = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=500)
    price = factory.Faker("random_int", min=1, max=10000)
    active = True

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
