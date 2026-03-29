from . import models, serializers
from .serializers import get_ordered_quantity
from dessertsbyseth import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
import stripe
import logging
from typing import cast

logger = logging.getLogger(__name__)

def post_generic(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_generic(model, token=None):
    if token is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        item_to_delete = model.objects.get(auth_token=token)
    except model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    item_to_delete.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# subscribe and unsubscribe from mailing list
class MailingListView(APIView):
    """
    Add email to mailing list
    """
    def post(self, request, token=None):
        serializer = serializers.MailingListSubscriberSerializer(data=request.data)
        return post_generic(serializer)

    def delete(self, request, token=None):
        return delete_generic(models.MailingListSubscriber, token)

# get products
class ProductView(APIView):
    def get(self, request):
        orders = models.Product.objects.filter(available=True)
        serializer = serializers.ProductSerializer(orders, many=True)
        return Response(serializer.data)

# view active preorder windows
class PreorderWindowView(APIView):
    def get(self, request):
        window = models.PreorderWindow.objects.filter(active=True)
        serializer = serializers.PreorderWindowSerializer(window, many=True)
        return Response(serializer.data)

class PreorderView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = serializers.WritePreorderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # check if order counts are valid
        items = serializer.validated_data["items"] # type: ignore
        preorder_window = serializer.validated_data['window'] # type: ignore
        # lock current row untnil transaction ends
        for listing in models.PreorderListing.objects.select_for_update().filter(window=preorder_window):
            for item in items:
                if item['product_listing'] == listing:
                    ordered = get_ordered_quantity(listing)
                    if (ordered + item['quantity'] > listing.limit):
                        return Response({"error": f"{listing.name} does not have enough remaining capacity"},
                                        status=status.HTTP_409_CONFLICT)
                    break
        order = cast(models.Preorder, serializer.save())
        try: 
            payment_intent = stripe.PaymentIntent.create(
                amount = int (order.total * 100),
                currency='usd',
                automatic_payment_methods={"enabled": True},
                metadata={'order_id': str(order.id)}
            )
        except stripe.StripeError:
            transaction.set_rollback(True)
            return Response({'error': "Payment processing unavailable"}, status=status.HTTP_502_BAD_GATEWAY)
        order.stripe_payment_intent_id = payment_intent.id
        order.stripe_payment_status = payment_intent.status
        order.save()

        data = dict(serializers.ReadPreorderSerializer(order).data)
        data['client_secret'] = payment_intent.client_secret
        return Response(data, status=status.HTTP_201_CREATED)

class PreorderStatusView(APIView):
    def get(self, request, id):
        try:
            preorder = models.Preorder.objects.get(pk=id)
        except models.Preorder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({"status": preorder.status})

# post custom order
class CustomOrderView(APIView):
    def post(self, request):
        serializer = serializers.CustomOrderRequestSerializer(data=request.data)
        return post_generic(serializer)

# subscribe and unsubscribe from guinea pig
class GuineaPigMembershipView(APIView):
    def post(self, request, token=None):
        serializer = serializers.GuineaPigSerializer(data=request.data)
        return post_generic(serializer)
    
    def delete(self, request, token=None):
        return delete_generic(models.GuineaPig, token)

# view drop
class GuineaPigDropView(APIView):
    def get(self, request, drop_id):
        try:
            drop = models.GuineaPigDrop.objects.get(pk=drop_id)
        except models.GuineaPigDrop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.GuineaPigDropSerializer(drop)
        return Response(serializer.data)

# add and cancel claim to a drop
class GuineaPigClaimView(APIView):
    @transaction.atomic
    def post(self, request, drop_id):
        serializer = serializers.GuineaPigClaimInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # check that Guinea Pig exists
        try:
            guinea_pig = models.GuineaPig.objects.get(auth_token=serializer.validated_data['auth_token'], active=True) # type: ignore
        except models.GuineaPig.DoesNotExist:
            return Response({"error": "email not registered as guinea pig"}, status=status.HTTP_404_NOT_FOUND)
        # check that drop exists
        try:
            drop = models.GuineaPigDrop.objects.select_for_update().get(pk=drop_id)
        except models.GuineaPigDrop.DoesNotExist:
            return Response({"error": "drop does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # check that the drop window is still open
        now = timezone.now()
        if now > drop.registration_until:
            return Response({"error": "drop window closed"}, status=status.HTTP_400_BAD_REQUEST)
        # check that drop is not full
        current_signup = models.GuineaPigClaim.objects.filter(drop=drop_id, canceled=False).count()
        if current_signup >= drop.total_slots:
            return Response({"message": "All drop slots claimed"}, status=status.HTTP_409_CONFLICT)
        try:
            claim = models.GuineaPigClaim.objects.get(drop=drop_id, guinea_pig=guinea_pig)
            if not claim.canceled:
                return Response({"error": "Drop already claimed"}, status=status.HTTP_409_CONFLICT)
            claim.canceled = False
            claim.pickup_time = serializer.validated_data['pickup_time'] # type: ignore
            claim.registered_at = now
            claim.save()
        except models.GuineaPigClaim.DoesNotExist:
            models.GuineaPigClaim.objects.create(
                drop = drop,
                guinea_pig = guinea_pig,
                pickup_time=serializer.validated_data['pickup_time'] # type: ignore
            )
        return Response(status=status.HTTP_201_CREATED)
        
    
    def patch(self, request, drop_id):
        serializer = serializers.GuineaPigAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "auth token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            guinea_pig = models.GuineaPig.objects.get(auth_token=serializer.validated_data['auth_token']) # type: ignore
        except models.GuineaPig.DoesNotExist:
            return Response({"error": "Not a register guinea pig"}, status=status.HTTP_404_NOT_FOUND)
        try:
            claim = models.GuineaPigClaim.objects.get(guinea_pig=guinea_pig, drop=drop_id)
            if claim.canceled:
                raise models.GuineaPigClaim.DoesNotExist
        except models.GuineaPigClaim.DoesNotExist:
            return Response({"error": "Claim not found"}, status=status.HTTP_404_NOT_FOUND)
        claim.canceled = True
        claim.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

### Stripe Views

class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.SignatureVerificationError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata'].get('order_id')
        event_type = event['type']
        updated = None
        
        if order_id is None:
            return Response({'success': True}, status=status.HTTP_200_OK)

        if event_type == 'payment_intent.succeeded':
            updated = models.Preorder.objects.filter(id=order_id).update(
                status=models.Preorder.CONFIRMED,
                stripe_payment_status=payment_intent['status']
            )
        elif event_type == 'payment_intent.payment_failed':
            updated = models.Preorder.objects.filter(id=order_id).update(
                status=models.Preorder.PENDING,
                stripe_payment_status=payment_intent['status']
            )
        elif event_type == 'payment_intent.canceled':
            updated = models.Preorder.objects.filter(id=order_id).update(
                status=models.Preorder.CANCELED,
                stripe_payment_status=payment_intent['status']
            )
        if updated is not None and updated == 0:                
            logger.error(f"{event_type} for unknown order_id={order_id}, intent={payment_intent['id']}")
            return Response({'error': 'Order not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True}, status=status.HTTP_200_OK)