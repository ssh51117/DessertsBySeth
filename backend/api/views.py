from . import models, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import get_ordered_quantity
from django.utils import timezone

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

# todo: add stripe integration
class PreorderView(APIView):
    def post(self, request):
        serializer = serializers.WritePreorderSerializer(data=request.data)
        if serializer.is_valid():
            # check if order counts are valid
            items = serializer.validated_data["items"] # type: ignore
            preorder_window = serializer.validated_data['window'] # type: ignore
            for listing in models.PreorderListing.objects.filter(window=preorder_window):
                for item in items:
                    if item['product'] == listing:
                        ordered = get_ordered_quantity(listing)
                        if (ordered + items['quantity'] > listing.limit):
                            return Response({"error": f"{listing.name} does not have enough remaining capacity"},
                                            status=status.HTTP_409_CONFLICT)
                        break
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def post(self, request, drop_id):
        serializer = serializers.GuineaPigClaimInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # check that Guinea Pig exists
        try:
            guinea_pig = models.GuineaPig.objects.get(auth_token=serializer.validated_data['auth_token']) # type: ignore
        except models.GuineaPig.DoesNotExist:
            return Response({"error": "email not registered as guinea pig"}, status=status.HTTP_404_NOT_FOUND)
        # check that drop exists
        try:
            drop = models.GuineaPigDrop.objects.get(pk=drop_id)
        except models.GuineaPigDrop.DoesNotExist:
            return Response({"error": "drop does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # check that the drop window is still open
        now = timezone.now()
        if now > drop.registration_until:
            return Response({"error": "drop window closed"}, status=status.HTTP_400_BAD_REQUEST)
        # check that drop is not full
        current_signup = models.GuineaPigClaim.objects.filter(drop=drop_id, cancelled=False).count()
        if current_signup >= drop.total_slots:
            return Response({"message": "All drop slots claimed"}, status=status.HTTP_409_CONFLICT)
        try:
            claim = models.GuineaPigClaim.objects.get(drop=drop_id, guinea_pig=guinea_pig)
            if not claim.cancelled:
                return Response({"error": "Drop already claimed"}, status=status.HTTP_409_CONFLICT)
            claim.cancelled = False
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
            claim = models.GuineaPigClaim.objects.get(guinea_pig=guinea_pig, drop=drop_id, cancelled=False)
        except models.GuineaPigClaim.DoesNotExist:
            return Response({"error": "Claim not found"}, status=status.HTTP_404_NOT_FOUND)
        claim.cancelled = True
        claim.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
