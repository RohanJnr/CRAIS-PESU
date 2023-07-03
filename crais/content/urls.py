from django.urls import path

from .views import MemberView, PatentsView, PublicationsView


urlpatterns = [
    path("publications", PublicationsView.as_view(), name="publications-list"),
    path("patents", PatentsView.as_view(), name="patents-list"),
    path("team/<str:slug>", MemberView.as_view(), name="member-detail")
]
