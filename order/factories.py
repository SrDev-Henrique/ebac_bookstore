# pyright: reportUnannotatedClassAttribute=false, reportPrivateImportUsage=false, reportUnknownMemberType=false

import factory
from django.contrib.auth.models import User

from order.models.order import Order
from product.factories import ProductFactory
from product.models.product import Product


class UserFactory(factory.django.DjangoModelFactory[User]):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class OrderFactory(factory.django.DjangoModelFactory[Order]):
    class Meta:
        model = Order
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(
        self,
        create: bool,
        extracted: list[Product] | None,
    ) -> None:
        if not create:
            return
        if extracted:
            for item in extracted:
                self.product.add(item)  # pyright: ignore[reportAttributeAccessIssue]
        else:
            self.product.add(ProductFactory())  # pyright: ignore[reportAttributeAccessIssue]
