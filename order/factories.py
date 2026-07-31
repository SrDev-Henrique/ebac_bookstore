import factory
from django.contrib.auth.models import User

from order.models import Order
from product.factories import ProductFactory


class UserFactory(factory.django.DjangoModelFactory[User]):
    username = factory.Faker("user_name")
    email = factory.Faker("email")

    class Meta:
        model = User


class OrderFactory(factory.django.DjangoModelFactory[Order]):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.product.add(item)  # pyright: ignore[reportAttributeAccessIssue]
        else:
            self.product.add(ProductFactory())  # pyright: ignore[reportAttributeAccessIssue]

    class Meta:
        model = Order
