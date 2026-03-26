from . import models, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def post_generic(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_generic(model, token=None):
    if token is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        item_to_delete = model.objects.get(unsubscribe_token=token)
    except model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    item_to_delete.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class MailingListView(APIView):
    """
    Add email to mailing list
    """
    def post(self, request, token=None):
        serializer = serializers.MailingListSubscriberSerializer(data=request.data)
        return post_generic(serializer)

    def delete(self, request, token=None):
        return delete_generic(models.MailingListSubscriber, token)

class GuineaPigMembershipView(APIView):
    def post(self, request, token=None):
        serializer = serializers.GuineaPigSerializer(data=request.data)
        return post_generic(serializer)
    
    def delete(self, request, token=None):
        return delete_generic(models.GuineaPig, token)
    
class GuineaPigClaimView(APIView):
    def post(self, request, drop_id):
        try:
            guinea_pig = models.GuineaPig.objects.get(email=request.data['email'])
        except models.GuineaPig.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['drop'] = drop_id
        data['guinea_pig'] = guinea_pig.pk
        serializer = serializers.GuineaPigClaimSerializer(data=data)
        return post_generic(serializer)
    
    def patch(self, request, drop_id):
        try:
            guinea_pig = models.GuineaPig.objects.get(email=request.data['email'])
            claim = models.GuineaPigClaim.objects.get(guinea_pig=guinea_pig)
        except (models.GuineaPig.DoesNotExist, models.GuineaPigClaim.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        claim.cancelled = True
        claim.save()
        return Response(status=status.HTTP_204_NO_CONTENT)