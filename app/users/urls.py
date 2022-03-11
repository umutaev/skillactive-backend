from django.urls import path

from .views import (
    CreateUserView,
    VerifyUser,
    Login,
    CheckStaff,
    RestoreUser,
    UserRestorationRequest,
)

urlpatterns = [
    path("auth/", Login.as_view()),
    path("register/", CreateUserView.as_view()),
    path("restoration_request/", UserRestorationRequest.as_view()),
    path("restore/", RestoreUser.as_view()),
    path("verify/<str:uid>/<str:token>", VerifyUser.as_view(), name="verify-account"),
    path("check_staff/", CheckStaff.as_view()),
]
