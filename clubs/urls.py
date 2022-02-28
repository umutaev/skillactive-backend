from webbrowser import get
from django.urls import path
from clubs.views import club, post_club, get_clubs_user, search_club
from applications.views import applications

urlpatterns = [
    path("", post_club),
    path("my/", get_clubs_user),
    path("<int:pk>/", club),
    path("search/", search_club),
    path("<int:pk>/applications", applications)
]