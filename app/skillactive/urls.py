from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("feed/", include("feed.urls")),
    path("users/", include("users.urls")),
    path("comments/", include("comments.urls")),
    path("clubs/", include("clubs.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("applications/", include("applications.urls")),
    path("categories/", include("categories.urls")),
    path("districts/", include("districts.urls")),
    path("organizations/", include("organizations.urls")),
]
