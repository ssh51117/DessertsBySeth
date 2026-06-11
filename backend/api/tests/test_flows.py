"""
User-flow integration tests: full HTTP round-trips against an in-memory DB.
External calls (Stripe, Resend) are patched only where needed.
"""
import pytest
import uuid
from unittest.mock import patch, MagicMock
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from api.tests.factories import (
    ProductFactory,
    PreorderWindowFactory,
    PreorderListingFactory,
    MailingListSubscriberFactory,
    GuineaPigFactory,
    GuineaPigDropFactory,
)
from api import models


# ---------------------------------------------------------------------------
# Preorder flow
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@patch("api.views.stripe.PaymentIntent.create")
def test_create_preorder_happy_path(mock_stripe, api_client, open_window, listing):
    mock_pi = MagicMock()
    mock_pi.id = "pi_test_abc"
    mock_pi.client_secret = "pi_test_abc_secret"
    mock_pi.status = "requires_payment_method"
    mock_stripe.return_value = mock_pi

    payload = {
        "window": open_window.id,
        "customer_name": "Jane Smith",
        "customer_email": "jane@example.com",
        "total": "12.00",
        "items": [{"product_listing": listing.id, "quantity": 1}],
    }
    response = api_client.post("/preorders/", payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert "client_secret" in data
    assert data["client_secret"] == "pi_test_abc_secret"

    order = models.Preorder.objects.get(stripe_payment_intent_id="pi_test_abc")
    assert order.customer_email == "jane@example.com"
    assert order.status == models.Preorder.PENDING


# ---------------------------------------------------------------------------
# Mailing list round-trip
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_mailing_list_subscribe(api_client):
    response = api_client.post("/mailing-list/", {"email": "hello@example.com"}, format="json")
    assert response.status_code == 201
    assert models.MailingListSubscriber.objects.filter(email="hello@example.com").exists()


@pytest.mark.django_db
def test_mailing_list_subscribe_duplicate_returns_400(api_client):
    MailingListSubscriberFactory(email="dupe@example.com")
    response = api_client.post("/mailing-list/", {"email": "dupe@example.com"}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_mailing_list_unsubscribe(api_client):
    sub = MailingListSubscriberFactory()
    response = api_client.delete(f"/mailing-list/{sub.auth_token}/")
    assert response.status_code == 204
    assert not models.MailingListSubscriber.objects.filter(pk=sub.pk).exists()


@pytest.mark.django_db
def test_mailing_list_unsubscribe_invalid_token_returns_404(api_client):
    response = api_client.delete(f"/mailing-list/{uuid.uuid4()}/")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Guinea pig membership round-trip
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_guinea_pig_register(api_client):
    response = api_client.post(
        "/guinea-pigs/",
        {"name": "Fluffy", "email": "fluffy@example.com"},
        format="json",
    )
    assert response.status_code == 201
    assert models.GuineaPig.objects.filter(email="fluffy@example.com").exists()


@pytest.mark.django_db
def test_guinea_pig_unregister(api_client, guinea_pig):
    response = api_client.delete(f"/guinea-pigs/{guinea_pig.auth_token}/")
    assert response.status_code == 204
    assert not models.GuineaPig.objects.filter(pk=guinea_pig.pk).exists()


# ---------------------------------------------------------------------------
# Guinea pig drop claim round-trip
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_get_guinea_pig_drop(api_client, open_drop):
    response = api_client.get(f"/guinea-pig-drops/{open_drop.id}/")
    assert response.status_code == 200
    assert response.json()["title"] == open_drop.title


@pytest.mark.django_db
def test_get_nonexistent_drop_returns_404(api_client):
    response = api_client.get("/guinea-pig-drops/99999/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_guinea_pig_claim_drop(api_client, guinea_pig, open_drop):
    pickup_time = (timezone.now() + timedelta(days=1)).isoformat()
    payload = {"auth_token": str(guinea_pig.auth_token), "pickup_time": pickup_time}
    response = api_client.post(f"/guinea-pig-drops/{open_drop.id}/claim/", payload, format="json")
    assert response.status_code == 201
    assert models.GuineaPigClaim.objects.filter(drop=open_drop, guinea_pig=guinea_pig).exists()


@pytest.mark.django_db
def test_guinea_pig_claim_duplicate_returns_409(api_client, guinea_pig, open_drop):
    pickup_time = (timezone.now() + timedelta(days=1)).isoformat()
    payload = {"auth_token": str(guinea_pig.auth_token), "pickup_time": pickup_time}
    api_client.post(f"/guinea-pig-drops/{open_drop.id}/claim/", payload, format="json")
    response = api_client.post(f"/guinea-pig-drops/{open_drop.id}/claim/", payload, format="json")
    assert response.status_code == 409


@pytest.mark.django_db
def test_guinea_pig_cancel_claim(api_client, guinea_pig, open_drop):
    pickup_time = (timezone.now() + timedelta(days=1)).isoformat()
    api_client.post(
        f"/guinea-pig-drops/{open_drop.id}/claim/",
        {"auth_token": str(guinea_pig.auth_token), "pickup_time": pickup_time},
        format="json",
    )
    response = api_client.patch(
        f"/guinea-pig-drops/{open_drop.id}/claim/",
        {"auth_token": str(guinea_pig.auth_token)},
        format="json",
    )
    assert response.status_code == 204
    claim = models.GuineaPigClaim.objects.get(drop=open_drop, guinea_pig=guinea_pig)
    assert claim.canceled is True


@pytest.mark.django_db
def test_guinea_pig_cancel_nonexistent_claim_returns_404(api_client, guinea_pig, open_drop):
    response = api_client.patch(
        f"/guinea-pig-drops/{open_drop.id}/claim/",
        {"auth_token": str(guinea_pig.auth_token)},
        format="json",
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Custom order round-trip
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_submit_custom_order(api_client):
    pickup_date = (timezone.now() + timedelta(days=7)).isoformat()
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "request_description": "Custom birthday cake",
        "requested_pickup_date": pickup_date,
    }
    response = api_client.post("/custom-order/", payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_submit_custom_order_past_date_returns_400(api_client):
    pickup_date = (timezone.now() - timedelta(days=1)).isoformat()
    payload = {
        "name": "Bob",
        "email": "bob@example.com",
        "request_description": "Cookies",
        "requested_pickup_date": pickup_date,
    }
    response = api_client.post("/custom-order/", payload, format="json")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Products endpoint
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_products_returns_only_available(api_client):
    ProductFactory(available=True, name="Visible Cake")
    ProductFactory(available=False, name="Hidden Pie")
    response = api_client.get("/products/")
    assert response.status_code == 200
    names = [p["name"] for p in response.json()]
    assert "Visible Cake" in names
    assert "Hidden Pie" not in names


# ---------------------------------------------------------------------------
# Preorder window endpoint
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_preorder_window_returns_active(api_client, open_window):
    response = api_client.get("/preorder-window/current/")
    assert response.status_code == 200
    ids = [w["id"] for w in response.json()]
    assert open_window.id in ids


@pytest.mark.django_db
def test_preorder_window_no_active_returns_empty(api_client):
    PreorderWindowFactory(active=False)
    response = api_client.get("/preorder-window/current/")
    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# Preorder status endpoint
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_preorder_status(api_client, pending_preorder):
    response = api_client.get(f"/preorders/{pending_preorder.id}/status/")
    assert response.status_code == 200
    assert response.json()["status"] == models.Preorder.PENDING


@pytest.mark.django_db
def test_preorder_status_not_found(api_client):
    response = api_client.get(f"/preorders/{uuid.uuid4()}/status/")
    assert response.status_code == 404
