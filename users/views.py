from django.http import HttpResponse
from django.contrib.auth import get_user_model
from users.tokens import account_activation_token
from django.http import JsonResponse, HttpResponse

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import permissions

from .serializers import UserSerializer


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
        print(uid, kwargs["token"])
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
