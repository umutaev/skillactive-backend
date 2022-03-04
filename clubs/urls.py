from webbrowser import get
from django.urls import path
from clubs.views import (
    club,
    post_club,
    get_clubs_user,
    search_club,
    ClubView,
    SpecificClubView,
)
from applications.views import applications, application

urlpatterns = [
    path("", ClubView.as_view()),
    path("<int:pk>/", SpecificClubView.as_view()),
    path("<int:pk>/applications", applications),
    path("<int:pk_club>/applications/<int:pk_application>", application),
]
