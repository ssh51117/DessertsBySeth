"""
Mailer service unit tests. All tests patch resend.Emails.send so no
real email credentials or network calls are needed.
"""
from unittest.mock import patch, call
from api.services import mailer


@patch("api.services.mailer.resend.Emails.send")
def test_send_order_confirmation_calls_resend_once(mock_send):
    mailer.send_order_confirmation(
        email="customer@example.com",
        name="Jane",
        order_id="order-uuid-123",
        pickup_date="June 14, 2026",
        location="Atlanta, GA",
        items=[{"name": "Chocolate Cake", "quantity": 1, "subtotal": 12}],
        total="12.00",
    )
    mock_send.assert_called_once()


@patch("api.services.mailer.resend.Emails.send")
def test_send_order_confirmation_to_correct_email(mock_send):
    mailer.send_order_confirmation(
        email="recipient@example.com",
        name="Jane",
        order_id="order-uuid-123",
        pickup_date="June 14, 2026",
        location="Atlanta, GA",
        items=[],
        total="0.00",
    )
    sent_args = mock_send.call_args[0][0]
    assert sent_args["to"] == "recipient@example.com"


@patch("api.services.mailer.resend.Emails.send")
def test_send_order_confirmation_subject_contains_confirmed(mock_send):
    mailer.send_order_confirmation(
        email="x@example.com",
        name="Jane",
        order_id="order-uuid-123",
        pickup_date="June 14, 2026",
        location="Atlanta, GA",
        items=[],
        total="0.00",
    )
    sent_args = mock_send.call_args[0][0]
    assert "Confirmed" in sent_args["subject"]


@patch("api.services.mailer.resend.Emails.send")
def test_send_order_confirmation_html_contains_order_id(mock_send):
    mailer.send_order_confirmation(
        email="x@example.com",
        name="Jane",
        order_id="specific-order-id-xyz",
        pickup_date="June 14, 2026",
        location="Atlanta, GA",
        items=[],
        total="0.00",
    )
    sent_args = mock_send.call_args[0][0]
    assert "specific-order-id-xyz" in sent_args["html"]


@patch("api.services.mailer.resend.Emails.send")
def test_send_guinea_pig_drop_notification_sends_per_email(mock_send):
    emails = ["a@example.com", "b@example.com", "c@example.com"]
    mailer.send_guinea_pig_drop_notification(
        emails=emails,
        drop_title="Summer Drop",
        drop_description="Delicious summer treats",
        registration_until="June 10, 2026",
        pickup_date="June 14, 2026",
        claim_url="https://example.com/claim",
    )
    assert mock_send.call_count == 3


@patch("api.services.mailer.resend.Emails.send")
def test_send_preorder_window_notification_sends_per_subscriber(mock_send):
    subscribers = [
        ("a@example.com", "token-aaa"),
        ("b@example.com", "token-bbb"),
        ("c@example.com", "token-ccc"),
        ("d@example.com", "token-ddd"),
    ]
    mailer.send_preorder_window_notification(
        emails=subscribers,
        pickup_date="June 14, 2026",
        closes_at="June 10, 2026",
        listings=[{"name": "Brownie", "unit_price": "8.00"}],
        order_url="https://example.com/cart",
        unsubscribe_base_url="https://example.com/unsubscribe",
    )
    assert mock_send.call_count == 4
    # Each email should contain its own unsubscribe token
    calls_html = [c[0][0]["html"] for c in mock_send.call_args_list]
    assert any("token-aaa" in html for html in calls_html)
    assert any("token-ddd" in html for html in calls_html)


@patch("api.services.mailer.resend.Emails.send")
def test_send_mailing_list_blast_sends_per_subscriber(mock_send):
    subscribers = [("x@example.com", "tok-x"), ("y@example.com", "tok-y")]
    mailer.send_mailing_list_blast(
        emails=subscribers,
        subject="Big news!",
        body="<p>Hello!</p>",
        unsubscribe_base_url="https://example.com/unsub",
    )
    assert mock_send.call_count == 2
    calls_html = [c[0][0]["html"] for c in mock_send.call_args_list]
    assert any("tok-x" in html for html in calls_html)
    assert any("tok-y" in html for html in calls_html)
