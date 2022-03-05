from webbrowser import get
from django.urls import path, include
from clubs.views import (
    ClubView,
    SpecificClubView,
)
from applications.views import applications, application

urlpatterns = [
    path("", ClubView.as_view()),
    path("<int:pk>/", SpecificClubView.as_view()),
    path("<int:club>/applications/", include("applications.clubs_urls")),
]
