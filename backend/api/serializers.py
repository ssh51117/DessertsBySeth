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
from django.db.models import Sum

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
        fields = ["title", "description", "available_from", "available_until", "total_slots", "notified_at", "registration_until"]
        read_only_fields = ["created_at"]

class GuineaPigAuthSerializer(serializers.Serializer):
    auth_token = serializers.UUIDField()

class GuineaPigClaimInputSerializer(GuineaPigAuthSerializer):
    pickup_time = serializers.DateTimeField()
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image"]

def get_ordered_quantity(listing):
    return PreorderItem.objects.filter(
            order__status__in = [Preorder.CONFIRMED, Preorder.FULFILLED],
            product=listing
        ).aggregate(total = Sum('quantity'))['total'] or 0

class PreorderListingSerializer(serializers.ModelSerializer):
    remaining = serializers.SerializerMethodField()
    class Meta:
        model = PreorderListing
        fields = ["name", "unit_price", "limit", "remaining"]
    
    def get_remaining(self, obj):
        return obj.limit - get_ordered_quantity(obj)

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