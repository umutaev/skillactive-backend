from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from users.email import send_restore_mail
from users.tokens import account_activation_token
from django.http import JsonResponse, HttpResponse

from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from users.serializers import (
    UserSerializer,
    AccountRestorationSerializer,
    AccountRestorationRequestSerializer,
    GrantStaffSerializer,
    UserProfileSerializer,
)
from users.email import send_activation_email
from users.models import UserProfile


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class VerifyUser(GenericAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = model.objects.all()

    def get(self, request, *args, **kwargs):
        uid = int(kwargs["uid"])
        user = self.get_queryset().filter(pk=uid).get()
        if account_activation_token.check_token(user, kwargs["token"]):
            print(account_activation_token.check_token(user, kwargs["token"]))
            user.is_active = True
            print(account_activation_token.check_token(user, kwargs["token"]))
            user.save()
            print(account_activation_token.check_token(user, kwargs["token"]))
            return JsonResponse(
                self.get_serializer(user).data,
                safe=False,
                json_dumps_params={"ensure_ascii": False},
            )
        else:
            return HttpResponse(status=400)


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        user = serializer.validated_data.get("user", None)
        if user is None:
            try:
                user = (
                    get_user_model()
                    .objects.filter(username=request.data.get("username"))
                    .get()
                )
                if not check_password(request.data.get("password"), user.password):
                    raise get_user_model().DoesNotExist
            except get_user_model().DoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"auth": "User does not exist"},
                )
            send_activation_email(user)
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"auth": "Check email"},
            )
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class CheckStaff(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_staff:
            return Response(data={"status": True})
        else:
            raise PermissionDenied


class UserRestorationRequest(GenericAPIView):
    serializer_class = AccountRestorationRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        try:
            user = (
                get_user_model()
                .objects.filter(email=serializer.validated_data["email"])
                .get()
            )
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        send_restore_mail(user)
        return Response(
            status=status.HTTP_200_OK,
            data={"auth": "Check email"},
        )


class RestoreUser(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountRestorationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = (
                get_user_model()
                .objects.filter(pk=serializer.validated_data["uid"])
                .get()
            )
        except:
            return Response(status=400)
        if account_activation_token.check_token(
            user, serializer.validated_data["token"]
        ):
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(status=204)
        else:
            return Response(status=400)


class MakeStaff(RetrieveAPIView, UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = GrantStaffSerializer
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        print(self.get_object())
        return super().retrieve(request, *args, **kwargs)


class ProfileView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = "owner"

    def update(self, request, *args, **kwargs):
        if not self.get_object().owner == request.user and not request.user.is_staff:
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self.get_object().owner == request.user and not request.user.is_staff:
            raise PermissionDenied
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.owner == request.user and not request.user.is_staff:
            raise PermissionDenied
        instance.owner.set_unusable_password()
        for club in instance.owner.clubs.all():
            club.opened = False
            club.save()
        try:
            instance.owner.auth_token.delete()
        except get_user_model().auth_token.RelatedObjectDoesNotExist:
            pass
        instance.save()
        return Response(status=204)
