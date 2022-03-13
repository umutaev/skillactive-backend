from django.urls import path
from organizations.views import OrganizationsView, OrganizationView

urlpatterns = [
    path("", OrganizationView.as_view()),
    path("list/", OrganizationsView.as_view()),
]
