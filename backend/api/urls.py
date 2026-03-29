from django.urls import path
from api import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("mailing-list/", views.MailingListView.as_view()),
    path("mailing-list/<uuid:token>/", views.MailingListView.as_view()),
    path("guinea-pigs/", views.GuineaPigMembershipView.as_view()),
    path("guinea-pigs/<uuid:token>/", views.GuineaPigMembershipView.as_view()),
    path("guinea-pig-drops/<int:drop_id>/", views.GuineaPigDropView.as_view()),
    path("guinea-pig-drops/<int:drop_id>/claim/", views.GuineaPigClaimView.as_view()),
    path("products/", views.ProductView.as_view()),
    path("preorders/", views.PreorderView.as_view()),
    path("preorders/<int:id>/status/", views.PreorderStatusView.as_view()),
    path("preorder-window/current/", views.PreorderWindowView.as_view()),
    path("custom-order/", views.CustomOrderView.as_view()),
    
    path("webhook/", csrf_exempt(views.StripeWebhookView.as_view())),
]