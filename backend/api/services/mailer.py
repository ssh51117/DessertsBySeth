from django.conf import settings
import resend

resend.api_key = settings.RESEND_SECRET_KEY

FROM_EMAIL = "Desserts By Seth <orders@dessertsbyseth.com>"

def _base_html(content: str) -> str:
    return f"""
    <div style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; padding: 32px; background-color: #fdf6ee; color: #2d4a2d;">
        <h1 style="font-size: 24px; margin-bottom: 4px;">Desserts By Seth</h1>
        <hr style="border: none; border-top: 1px solid #2d4a2d; opacity: 0.25; margin-bottom: 24px;" />
        {content}
        <hr style="border: none; border-top: 1px solid #2d4a2d; opacity: 0.25; margin-top: 32px;" />
        <p style="font-size: 12px; color: #888; margin-top: 8px;">Desserts By Seth &mdash; Atlanta, GA</p>
    </div>
    """

def send_order_confirmation(email: str, name: str, order_id: str, pickup_date: str, location: str, items: list, total: str):
    rows = "".join(
        f"""<tr>
            <td style="padding: 6px 0;">{item['name']}</td>
            <td style="padding: 6px 0; text-align: center;">{item['quantity']}</td>
            <td style="padding: 6px 0; text-align: right;">${item['subtotal']}</td>
        </tr>"""
        for item in items
    )

    content = f"""
        <h2 style="font-size: 20px;">Order Confirmed</h2>
        <p>Hi {name}, your order has been confirmed. See you at pickup!</p>

        <p><strong>Pickup Code:</strong> {order_id}</p>
        <p><strong>Pickup Date:</strong> {pickup_date}</p>
        <p><strong>Location:</strong> {location}</p>

        <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">
            <thead>
                <tr style="border-bottom: 1px solid #2d4a2d;">
                    <th style="text-align: left; padding-bottom: 8px;">Item</th>
                    <th style="text-align: center; padding-bottom: 8px;">Qty</th>
                    <th style="text-align: right; padding-bottom: 8px;">Subtotal</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
            <tfoot>
                <tr style="border-top: 1px solid #2d4a2d;">
                    <td colspan="2" style="padding-top: 8px; font-weight: bold;">Total</td>
                    <td style="padding-top: 8px; text-align: right; font-weight: bold;">${total}</td>
                </tr>
            </tfoot>
        </table>

        <p style="margin-top: 24px;">Questions? Reply to this email or reach out at <a href="mailto:hello@dessertsbyseth.com" style="color: #2d4a2d;">hello@dessertsbyseth.com</a>.</p>
    """

    resend.Emails.send({
        "from": FROM_EMAIL,
        "to": email,
        "subject": "Your Desserts By Seth Order is Confirmed",
        "html": _base_html(content)
    })

#guinea pig drop notification
def send_guinea_pig_drop_notification(emails: list[str], drop_title: str, drop_description: str, registration_until: str, pickup_date: str, claim_url: str):
    content = f"""
        <h2 style="font-size: 20px;">A New Drop is Available</h2>
        <p>Hi! A new guinea pig drop has opened up.</p>

        <h3 style="font-size: 16px; margin-bottom: 4px;">{drop_title}</h3>
        <p style="margin-top: 0;">{drop_description}</p>

        <p><strong>Register by:</strong> {registration_until}</p>
        <p><strong>Pickup date:</strong> {pickup_date}</p>

        <a href="{claim_url}" style="display: inline-block; margin-top: 16px; padding: 10px 20px; background-color: #2d4a2d; color: #fdf6ee; text-decoration: none; border-radius: 4px; font-weight: bold;">
            Claim Your Slot
        </a>

        <p style="margin-top: 24px; font-size: 12px; color: #888;">
            You're receiving this because you're a registered guinea pig tester. Ty
        </p>
    """

    for email in emails:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": email,
            "subject": f"New Drop: {drop_title}",
            "html": _base_html(content)
        })

# preorder window format
def send_preorder_window_notification(emails: list[tuple], pickup_date: str, closes_at: str, listings: list, order_url: str, unsubscribe_base_url: str):
    rows = "".join(
        f"<tr><td style='padding: 6px 0;'>{listing['name']}</td><td style='padding: 6px 0; text-align: right;'>${listing['unit_price']}</td></tr>"
        for listing in listings
    )

    for email, token in emails:
        unsubscribe_url = f"{unsubscribe_base_url}/{token}/"
        content = f"""
            <h2 style="font-size: 20px;">A New Preorder Window is Open!</h2>
            <p>Orders are now open for pickup on <strong>{pickup_date}</strong>. Order by <strong>{closes_at}</strong>.</p>

            <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">
                <thead>
                    <tr style="border-bottom: 1px solid #2d4a2d;">
                        <th style="text-align: left; padding-bottom: 8px;">Item</th>
                        <th style="text-align: right; padding-bottom: 8px;">Price</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>

            <a href="{order_url}" style="display: inline-block; margin-top: 24px; padding: 10px 20px; background-color: #2d4a2d; color: #fdf6ee; text-decoration: none; border-radius: 4px; font-weight: bold;">
                Order Now
            </a>

            <p style="margin-top: 32px; font-size: 12px; color: #888;">
                You're receiving this because you subscribed to the Desserts By Seth mailing list.<br/>
                <a href="{unsubscribe_url}" style="color: #888;">Unsubscribe</a>
            </p>
        """
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": email,
            "subject": f"Preorders are open — pickup {pickup_date}",
            "html": _base_html(content)
        })


# custom mailing list
def send_mailing_list_blast(emails: list[tuple], subject: str, body: str, unsubscribe_base_url: str):
    for email, token in emails:
        unsubscribe_url = f"{unsubscribe_base_url}/{token}/"
        content = f"""
            {body}
            <p style="margin-top: 32px; font-size: 12px; color: #888;">
                You're receiving this because you subscribed to the Desserts By Seth mailing list.<br/>
                <a href="{unsubscribe_url}" style="color: #888;">Unsubscribe</a>
            </p>
        """
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": email,
            "subject": subject,
            "html": _base_html(content)
        })
