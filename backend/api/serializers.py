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
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

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
    def validate_pickup_time(self, pickup_time):
        if pickup_time <= timezone.now():
            raise serializers.ValidationError("pickup date must be in the future")
        return pickup_time
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image"]

def get_ordered_quantity(listing):
    return PreorderItem.objects.filter(
            order__status__in = [Preorder.CONFIRMED, Preorder.FULFILLED],
            product_listing=listing
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
        fields = ["product_listing", "quantity"]

class WritePreorderSerializer(serializers.ModelSerializer):
    items = PreorderItemSerializer(many=True)
    class Meta:
        model = Preorder
        fields = ["window", "customer_name", "customer_email", "customer_phone", "total", "items"]
        read_only_fields = ['stripe_payment_intent_id', 'stripe_payment_status']
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Preorder.objects.create(**validated_data)
        for item in items_data:
            PreorderItem.objects.create(order=order, **item)
        return order
    def validate(self, data):
        if timezone.now() > data['window'].closes_at:
            raise serializers.ValidationError({'window': "Preorder window has closed"})
        elif timezone.now() < data['window'].opens_at:
            raise serializers.ValidationError({'window': "Preorder window has not opened yet"})
        elif not data['window'].active:
            raise serializers.ValidationError({'window': "Preorder window not active"})
        if not data['items']:
            raise serializers.ValidationError({'items': "Order must contain at least one item."})
        total = 0
        for item in data['items']:
            if item["product_listing"].window != data['window']:
                raise serializers.ValidationError({'items': "Ordered items must be from the order's drop"})
            if item['quantity'] <= 0:
                raise serializers.ValidationError({'items': "Ordered item must have count greater than zero"})
            total += item['quantity'] * item['product_listing'].unit_price
        if total != data['total']:
            raise serializers.ValidationError({'total': "Total does not match calculated total"})
        return data

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
    def validate_requested_pickup_date(self, requested_pickup_date):
        if timezone.now() >= requested_pickup_date:
            raise serializers.ValidationError({"requested pickup date": "Pickup date must be in the future"})
        return requested_pickup_date