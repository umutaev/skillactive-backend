from django.urls import path
from rest_framework.authtoken import views

from .views import CreateUserView, VerifyUser, Login

urlpatterns = [
    path("auth/", Login.as_view()),
    path("register/", CreateUserView.as_view()),
    path("verify/<str:uid>/<str:token>", VerifyUser.as_view(), name="verify-account"),
]
