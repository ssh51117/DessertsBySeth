from .models import (
    MailingListSubscriber,
    GuineaPig,
    GuineaPigDrop,
    GuineaPigClaim,
    Product,
    PreorderWindow,
    PreorderListing,
    Preorder,
    PreorderItem,
    CustomOrderRequest,
)
from rest_framework import serializers

class MailingListSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingListSubscriber
        fields = ["email"]
        read_only_fields = ["subscribed_at"]

class GuineaPigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuineaPig
        fields = ["name", "email", "notes"]
        read_only_fields = ["subscribed_at", "active"]

class GuineaPigDropSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuineaPigDrop
        fields = ["title", "description", "available_from", "available_until", "total_slots", "notified_at"]
        read_only_fields = ["created_at"]

class GuineaPigClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuineaPigClaim
        fields = ["drop", "guinea_pig", "pickup_time", "cancelled"]
        read_only_fields = ["registered_at"]
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image"]

class PreorderListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreorderListing
        fields = ["name", "unit_price", "limit"]

class PreorderWindowSerializer(serializers.ModelSerializer):
    listings = PreorderListingSerializer(many=True)
    class Meta:
        model = PreorderWindow
        fields = ["opens_at", "closes_at", "pickup_date", "active", "listings"]


class PreorderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreorderItem
        fields = ["product", "quantity"]

class WritePreorderSerializer(serializers.ModelSerializer):
    items = PreorderItemSerializer(many=True)
    class Meta:
        model = Preorder
        fields = ["window", "customer_name", "customer_email", "customer_phone", "total", "items"]
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Preorder.objects.create(**validated_data)
        for item in items_data:
            PreorderItem.objects.create(order=order, **item)
        return order

class PreorderWindowSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreorderWindow
        fields = ["pickup_date"]

class ReadPreorderSerializer(serializers.ModelSerializer):
    window = PreorderWindowSummarySerializer()
    items = PreorderItemSerializer(many=True)
    
    class Meta:
        model = Preorder
        fields = ["window", "customer_name", "customer_email", "customer_phone",
                             "stripe_payment_status", "total", "items"]
        
class CustomOrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrderRequest
        fields = ["name", "email", "request_description", "requested_pickup_date", "delivery_details"]
        read_only_fields = ["submitted_at", "status"]