from django.urls import path
from api import views

urlpatterns = [
    path("mailing-list/", views.MailingListView.as_view()),
    path("mailing-list/<uuid:token>/", views.MailingListView.as_view()),
    path("guinea-pigs/", views.GuineaPigMembershipView.as_view()),
    path("guinea-pigs/<uuid:token>/", views.GuineaPigMembershipView.as_view()),
    path("guinea-pig-drops/<int:drop_id>/claim/", views.GuineaPigClaimView.as_view())
]