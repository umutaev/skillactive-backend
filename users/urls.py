from django.urls import path
from rest_framework.authtoken import views

from .views import CreateUserView, VerifyUser

urlpatterns = [
    path("auth/", views.obtain_auth_token),
    path("register/", CreateUserView.as_view()),
    path("verify/<str:uid>/<str:token>", VerifyUser.as_view(), name="verify-account"),
]
