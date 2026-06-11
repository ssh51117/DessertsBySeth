import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from api import models


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = "A test dessert"
    price = Decimal("12.00")
    available = True
    image = "https://example.com/image.jpg"


class PreorderWindowFactory(DjangoModelFactory):
    class Meta:
        model = models.PreorderWindow

    opens_at = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=1))
    closes_at = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=24))
    pickup_date = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=7)).date())
    active = True
    location = "Atlanta, GA"
    type = models.PreorderWindow.REGULAR


class PreorderListingFactory(DjangoModelFactory):
    class Meta:
        model = models.PreorderListing

    window = factory.SubFactory(PreorderWindowFactory)
    product = factory.SubFactory(ProductFactory)
    name = factory.LazyAttribute(lambda o: o.product.name)
    unit_price = factory.LazyAttribute(lambda o: o.product.price)
    limit = 10


class PreorderFactory(DjangoModelFactory):
    class Meta:
        model = models.Preorder

    window = factory.SubFactory(PreorderWindowFactory)
    customer_name = "Test Customer"
    customer_email = "test@example.com"
    total = Decimal("12.00")
    status = models.Preorder.PENDING


class MailingListSubscriberFactory(DjangoModelFactory):
    class Meta:
        model = models.MailingListSubscriber

    email = factory.Sequence(lambda n: f"subscriber{n}@example.com")


class GuineaPigFactory(DjangoModelFactory):
    class Meta:
        model = models.GuineaPig

    name = factory.Sequence(lambda n: f"Guinea Pig {n}")
    email = factory.Sequence(lambda n: f"guinea{n}@example.com")
    active = True


class GuineaPigDropFactory(DjangoModelFactory):
    class Meta:
        model = models.GuineaPigDrop

    title = "Test Drop"
    description = "A test guinea pig drop"
    available_from = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=1))
    available_until = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))
    registration_until = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=2))
    total_slots = 5
