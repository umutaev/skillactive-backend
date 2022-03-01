from django.urls import path
from rest_framework.authtoken import views

from .views import CreateUserView

urlpatterns = [
    path("auth/", views.obtain_auth_token),
    path("register/", CreateUserView.as_view()),
]
