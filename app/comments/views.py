from django.views.decorators.csrf import csrf_exempt
from comments.models import CommentModel
from comments.serializers import CommentSerializer
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CommentView(
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    GenericAPIView,
):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(description="Get a specific comment by primary key.")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Post a reply on a specific comment with specified primary key."
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(description="Edit a specific comment by primary key.")
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(description="Delete a specific comment by primary key.")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def comment(request, pk):
    comment = get_object_or_404(CommentModel, pk=pk)
    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data, safe=True)
    elif request.method == "PUT":
        if not (request.user.is_staff or comment.user == request.user):
            raise PermissionDenied
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, json_dumps_params={"ensure_ascii": False}
            )
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        if not (request.user.is_staff or comment.user == request.user):
            raise PermissionDenied
        comment.text = ""
        comment.title = None
        comment.images = []
        comment.rating = None
        comment.user = None
        comment.deleted = True
        comment.save()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(["POST"])
def post_comment(request, pk):
    if pk is None:
        return HttpResponseNotFound

    data = JSONParser().parse(request)

    original_comment = get_object_or_404(CommentModel, pk=pk)
    data["feed_item"] = original_comment.feed_item.pk

    data["reply_to"] = pk
    data["type"] = CommentModel.Type.ANSWER

    user = request.user
    if type(user) == AnonymousUser:
        data["anonymous"] = True
    else:
        data["user"] = user.pk

    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            serializer.data, status=201, json_dumps_params={"ensure_ascii": False}
        )
    return JsonResponse(serializer.errors, status=400)
