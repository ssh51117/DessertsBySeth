"""
Inventory edge-case tests: capacity checks, window validation, Stripe error rollback.
"""
import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from api.tests.factories import (
    PreorderWindowFactory,
    PreorderListingFactory,
    PreorderFactory,
    GuineaPigFactory,
    GuineaPigDropFactory,
)
from api import models


def _make_stripe_mock():
    mock_pi = MagicMock()
    mock_pi.id = "pi_test_inv"
    mock_pi.client_secret = "pi_test_inv_secret"
    mock_pi.status = "requires_payment_method"
    return mock_pi


# ---------------------------------------------------------------------------
# Capacity checks
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@patch("api.views.stripe.PaymentIntent.create")
def test_preorder_exceeds_capacity_returns_409(mock_stripe, api_client, open_window, listing):
    # Fill listing to its limit with confirmed orders
    for _ in range(listing.limit):
        order = PreorderFactory(
            window=open_window,
            total=Decimal("12.00"),
            status=models.Preorder.CONFIRMED,
        )
        models.PreorderItem.objects.create(order=order, product_listing=listing, quantity=1)

    payload = {
        "window": open_window.id,
        "customer_name": "Late Buyer",
        "customer_email": "late@example.com",
        "total": "12.00",
        "items": [{"product_listing": listing.id, "quantity": 1}],
    }
    response = api_client.post("/preorders/", payload, format="json")

    assert response.status_code == 409
    mock_stripe.assert_not_called()


@pytest.mark.django_db
@patch("api.views.stripe.PaymentIntent.create")
def test_preorder_stripe_error_rolls_back(mock_stripe, api_client, open_window, listing):
    import stripe as stripe_lib
    mock_stripe.side_effect = stripe_lib.StripeError("payment error")

    payload = {
        "window": open_window.id,
        "customer_name": "Stripe Fail",
        "customer_email": "fail@example.com",
        "total": "12.00",
        "items": [{"product_listing": listing.id, "quantity": 1}],
    }
    response = api_client.post("/preorders/", payload, format="json")

    assert response.status_code == 502
    assert not models.Preorder.objects.filter(customer_email="fail@example.com").exists()


# ---------------------------------------------------------------------------
# Window validation
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@patch("api.views.stripe.PaymentIntent.create")
def test_preorder_closed_window_returns_400(mock_stripe, api_client):
    closed_window = PreorderWindowFactory(
        opens_at=timezone.now() - timedelta(hours=48),
        closes_at=timezone.now() - timedelta(hours=1),
    )
    closed_listing = PreorderListingFactory(window=closed_window, unit_price=Decimal("12.00"))

    payload = {
        "window": closed_window.id,
        "customer_name": "Too Late",
        "customer_email": "toolate@example.com",
        "total": "12.00",
        "items": [{"product_listing": closed_listing.id, "quantity": 1}],
    }
    response = api_client.post("/preorders/", payload, format="json")

    assert response.status_code == 400
    mock_stripe.assert_not_called()


@pytest.mark.django_db
@patch("api.views.stripe.PaymentIntent.create")
def test_preorder_inactive_window_returns_400(mock_stripe, api_client):
    inactive_window = PreorderWindowFactory(active=False)
    inactive_listing = PreorderListingFactory(window=inactive_window, unit_price=Decimal("12.00"))

    payload = {
        "window": inactive_window.id,
        "customer_name": "Inactive",
        "customer_email": "inactive@example.com",
        "total": "12.00",
        "items": [{"product_listing": inactive_listing.id, "quantity": 1}],
    }
    response = api_client.post("/preorders/", payload, format="json")

    assert response.status_code == 400
    mock_stripe.assert_not_called()


@pytest.mark.django_db
@patch("api.views.stripe.PaymentIntent.create")
def test_preorder_mismatched_total_returns_400(mock_stripe, api_client, open_window, listing):
    payload = {
        "window": open_window.id,
        "customer_name": "Wrong Total",
        "customer_email": "wrong@example.com",
        "total": "99.99",  # does not match listing.unit_price * 1
        "items": [{"product_listing": listing.id, "quantity": 1}],
    }
    response = api_client.post("/preorders/", payload, format="json")

    assert response.status_code == 400
    mock_stripe.assert_not_called()


# ---------------------------------------------------------------------------
# Drop slot limits
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_guinea_pig_drop_full_returns_409(api_client, guinea_pig, open_drop):
    # Fill every slot with other guinea pigs
    for _ in range(open_drop.total_slots):
        other_gp = GuineaPigFactory()
        models.GuineaPigClaim.objects.create(
            drop=open_drop,
            guinea_pig=other_gp,
            pickup_time=timezone.now() + timedelta(days=1),
            canceled=False,
        )

    pickup_time = (timezone.now() + timedelta(days=1)).isoformat()
    response = api_client.post(
        f"/guinea-pig-drops/{open_drop.id}/claim/",
        {"auth_token": str(guinea_pig.auth_token), "pickup_time": pickup_time},
        format="json",
    )
    assert response.status_code == 409


@pytest.mark.django_db
def test_guinea_pig_drop_registration_closed_returns_400(api_client, guinea_pig):
    closed_drop = GuineaPigDropFactory(
        registration_until=timezone.now() - timedelta(hours=1)
    )
    pickup_time = (timezone.now() + timedelta(days=1)).isoformat()
    response = api_client.post(
        f"/guinea-pig-drops/{closed_drop.id}/claim/",
        {"auth_token": str(guinea_pig.auth_token), "pickup_time": pickup_time},
        format="json",
    )
    assert response.status_code == 400
