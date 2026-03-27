from django.db import models
from django.utils import timezone
import uuid


### Mailing List Tables

class MailingListSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False)

### Guinea Pig Tables

class GuineaPig(models.Model):
    name = models.CharField()
    email = models.EmailField(unique=True)
    notes = models.TextField(null=True, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False)

class GuineaPigDrop(models.Model):
    title = models.CharField()
    description = models.TextField()
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()
    total_slots = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    notified_at = models.DateTimeField(blank=True, null=True)
    registration_until = models.DateTimeField()

class GuineaPigClaim(models.Model):
    drop = models.ForeignKey(GuineaPigDrop, on_delete=models.CASCADE)
    guinea_pig = models.ForeignKey(GuineaPig, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField()
    registered_at = models.DateTimeField(default=timezone.now)
    cancelled = models.BooleanField(default=False)

    class Meta:
        unique_together = ("drop", "guinea_pig")


### Product Table


class Product(models.Model):
    name = models.CharField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField()
    # eventually switch this to an ImageField with S3 (requires MEDIA_ROOT config in settings and the Pillow Library)
    image = models.CharField()


### Preorder Tables

class PreorderWindow(models.Model):
    REGULAR = "R"
    POPUP = "P"
    WINDOW_TYPE = [
        (REGULAR, "Regular"),
        (POPUP, "Pop-up")
    ]
    opens_at = models.DateTimeField()
    closes_at = models.DateTimeField()
    pickup_date = models.DateField()
    active = models.BooleanField()
    location = models.CharField(blank=True, default="")
    type = models.CharField(choices=WINDOW_TYPE, default=REGULAR)

class PreorderListing(models.Model):
    window = models.ForeignKey(PreorderWindow, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    limit = models.IntegerField()

class Preorder(models.Model):
    PENDING = "P"
    CONFIRMED = "C"
    FULFILLED = "F"
    CANCELLED = "X"
    STATUS_OPTIONS = [
        (PENDING, "Pending Payment"),
        (CONFIRMED, "Confirmed"),
        (FULFILLED, "Fulfilled"),
        (CANCELLED, "Cancelled"),
    ]
    
    window = models.ForeignKey(PreorderWindow, on_delete=models.CASCADE)
    customer_name = models.CharField()
    customer_email = models.EmailField()
    customer_phone = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_OPTIONS, default=PENDING)
    stripe_payment_intent_id = models.CharField(unique=True, null=True, blank=True)
    stripe_payment_status = models.CharField(blank=True, default="")
    total = models.DecimalField(max_digits=6, decimal_places=2)

class PreorderItem(models.Model):
    order = models.ForeignKey(Preorder, models.CASCADE, related_name="items")
    product = models.ForeignKey(PreorderListing, models.CASCADE)
    quantity = models.IntegerField()

class CustomOrderRequest(models.Model):
    NEW = "N"
    IN_REVIEW = "R"
    ACCEPTED = "A"
    DECLINED = "D"
    COMPLETE = "C"
    CUSTOMER_ORDER_STATUS = [
        (NEW, "New Order"),
        (IN_REVIEW, "In Review"),
        (ACCEPTED, "Accepted"),
        (DECLINED, "Declined"),
        (COMPLETE, "Complete")
    ]
    name = models.CharField()
    email = models.EmailField()
    request_description = models.TextField()
    requested_pickup_date = models.DateTimeField()
    delivery_details = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CUSTOMER_ORDER_STATUS, default=NEW)