from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from users.tokens import account_activation_token
from django.http import JsonResponse, HttpResponse

from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from users.serializers import UserSerializer
from users.email import send_activation_email


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
            user.is_active = True
            user.save()
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
