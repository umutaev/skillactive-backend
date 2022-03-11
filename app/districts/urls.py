from django.urls import path
from districts.views import DistricsView, DistricView

urlpatterns = [
    path("", DistricsView.as_view()),
    path("<int:pk>/", DistricView.as_view()),
]
