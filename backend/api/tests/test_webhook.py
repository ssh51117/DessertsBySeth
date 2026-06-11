"""
Stripe webhook handler tests. All tests mock construct_event to bypass
signature verification so no real Stripe credentials are needed.
"""
import pytest
from unittest.mock import patch
from decimal import Decimal

from api.tests.factories import PreorderFactory, PreorderListingFactory
from api import models


def _make_event(event_type, order_id=None, pi_status="succeeded"):
    metadata = {"order_id": str(order_id)} if order_id is not None else {}
    return {
        "type": event_type,
        "data": {
            "object": {
                "id": "pi_test_webhook",
                "status": pi_status,
                "metadata": metadata,
            }
        },
    }


@pytest.fixture
def confirmed_order(open_window, listing):
    order = PreorderFactory(
        window=open_window,
        total=Decimal("12.00"),
        status=models.Preorder.PENDING,
        stripe_payment_intent_id="pi_test_webhook",
    )
    models.PreorderItem.objects.create(order=order, product_listing=listing, quantity=1)
    return order


def _post_webhook(api_client, event):
    return api_client.post(
        "/webhook/",
        event,
        format="json",
        HTTP_STRIPE_SIGNATURE="t=fake,v1=fake",
    )


# ---------------------------------------------------------------------------
# payment_intent.succeeded
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
@patch("api.views.mailer.send_order_confirmation")
def test_webhook_succeeded_confirms_order(mock_mailer, mock_construct, api_client, confirmed_order):
    mock_construct.return_value = _make_event("payment_intent.succeeded", confirmed_order.id)

    response = _post_webhook(api_client, {})

    assert response.status_code == 200
    confirmed_order.refresh_from_db()
    assert confirmed_order.status == models.Preorder.CONFIRMED
    mock_mailer.assert_called_once()


@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
@patch("api.views.mailer.send_order_confirmation")
def test_webhook_succeeded_mailer_failure_still_confirms(mock_mailer, mock_construct, api_client, confirmed_order):
    mock_construct.return_value = _make_event("payment_intent.succeeded", confirmed_order.id)
    mock_mailer.side_effect = Exception("Resend is down")

    response = _post_webhook(api_client, {})

    assert response.status_code == 200
    confirmed_order.refresh_from_db()
    assert confirmed_order.status == models.Preorder.CONFIRMED


# ---------------------------------------------------------------------------
# payment_intent.payment_failed
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
def test_webhook_payment_failed_keeps_pending(mock_construct, api_client, confirmed_order):
    mock_construct.return_value = _make_event(
        "payment_intent.payment_failed", confirmed_order.id, pi_status="requires_payment_method"
    )

    response = _post_webhook(api_client, {})

    assert response.status_code == 200
    confirmed_order.refresh_from_db()
    assert confirmed_order.status == models.Preorder.PENDING
    assert confirmed_order.stripe_payment_status == "requires_payment_method"


# ---------------------------------------------------------------------------
# payment_intent.canceled
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
def test_webhook_canceled_marks_order_canceled(mock_construct, api_client, confirmed_order):
    mock_construct.return_value = _make_event(
        "payment_intent.canceled", confirmed_order.id, pi_status="canceled"
    )

    response = _post_webhook(api_client, {})

    assert response.status_code == 200
    confirmed_order.refresh_from_db()
    assert confirmed_order.status == models.Preorder.CANCELED


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
def test_webhook_invalid_signature_returns_403(mock_construct, api_client):
    import stripe as stripe_lib
    mock_construct.side_effect = stripe_lib.SignatureVerificationError("bad sig", "header")

    response = _post_webhook(api_client, {})

    assert response.status_code == 403


@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
def test_webhook_unknown_event_type_returns_200(mock_construct, api_client):
    mock_construct.return_value = _make_event("customer.created")

    response = _post_webhook(api_client, {})

    assert response.status_code == 200


@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
def test_webhook_succeeded_unknown_order_returns_500(mock_construct, api_client):
    import uuid
    mock_construct.return_value = _make_event("payment_intent.succeeded", uuid.uuid4())

    response = _post_webhook(api_client, {})

    assert response.status_code == 500


@pytest.mark.django_db
@patch("api.views.stripe.Webhook.construct_event")
def test_webhook_no_order_id_in_metadata_returns_200(mock_construct, api_client):
    mock_construct.return_value = _make_event("payment_intent.succeeded", order_id=None)

    response = _post_webhook(api_client, {})

    assert response.status_code == 200
