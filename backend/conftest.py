import pytest
from rest_framework.test import APIClient
from decimal import Decimal
from api.tests.factories import (
    PreorderWindowFactory,
    PreorderListingFactory,
    PreorderFactory,
    GuineaPigFactory,
    GuineaPigDropFactory,
)
from api import models


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def open_window():
    return PreorderWindowFactory()


@pytest.fixture
def listing(open_window):
    return PreorderListingFactory(window=open_window, unit_price=Decimal("12.00"), limit=10)


@pytest.fixture
def sold_out_listing(open_window):
    return PreorderListingFactory(window=open_window, unit_price=Decimal("12.00"), limit=0)


@pytest.fixture
def pending_preorder(open_window, listing):
    order = PreorderFactory(
        window=open_window,
        total=Decimal("12.00"),
        status=models.Preorder.PENDING,
        stripe_payment_intent_id="pi_test_pending",
    )
    models.PreorderItem.objects.create(order=order, product_listing=listing, quantity=1)
    return order


@pytest.fixture
def guinea_pig():
    return GuineaPigFactory()


@pytest.fixture
def open_drop():
    return GuineaPigDropFactory()
