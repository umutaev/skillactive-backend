from django.views.decorators.csrf import csrf_exempt
from feed.models import FeedModel
from feed.serializers import FeedSerialier
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.db.models import F
from comments.models import CommentModel
from comments.serializers import CommentSerializer
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class FeedView(ListAPIView, CreateAPIView):
    queryset = FeedModel.objects.all()
    serializer_class = FeedSerialier
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        print(args, kwargs)
        if not request.user.is_staff:
            raise PermissionDenied
        return super().create(request, *args, **kwargs)


class FeedRecordView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = FeedModel.objects.all()
    serializer_class = FeedSerialier
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)


class ViewRequest(GenericAPIView):
    queryset = FeedModel.objects.all()
    lookup_field = "pk"
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        feed_item = self.get_object()
        feed_item.views_amount = F("views_amount") + 1
        feed_item.save()
        feed_item = self.get_object()
        return Response(status=204)


class ViewRequest(GenericAPIView):
    queryset = FeedModel.objects.all()
    lookup_field = "pk"
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        feed_item = self.get_object()
        feed_item.views_amount = F("views_amount") + 1
        feed_item.save()
        return Response(status=204)


class LikeRequest(GenericAPIView):
    queryset = FeedModel.objects.all()
    lookup_field = "pk"
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "action",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                required=True,
                description='upvote if action is "+", downvote if action is "-"',
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        feed_item = self.get_object()
        if request.query_params["action"] == "+":
            feed_item.likes_amount = F("likes_amount") + 1
        elif request.query_params["action"] == "-":
            feed_item.likes_amount = F("likes_amount") - 1
        feed_item.save()
        return Response(status=204)


@csrf_exempt
@api_view(["GET", "POST"])
def feed_list(request):
    print(request.user)
    if request.method == "GET":

        feed = FeedModel.objects.all()
        serializer = FeedSerialier(feed, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        if not request.user.is_staff:
            raise PermissionDenied
        data = JSONParser().parse(request)
        serializer = FeedSerialier(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, status=201, json_dumps_params={"ensure_ascii": False}
            )
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def feed_detail(request, pk):
    try:
        feed_object = FeedModel.objects.get(pk=pk)
    except FeedModel.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = FeedSerialier(feed_object)
        return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})

    elif request.method == "PUT":
        if not request.user.is_staff:
            raise PermissionDenied
        data = JSONParser().parse(request)
        serializer = FeedSerialier(feed_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, json_dumps_params={"ensure_ascii": False}
            )
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        if not request.user.is_staff:
            raise PermissionDenied
        feed_object.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(["GET"])
def get_comments(request, feed_pk):
    if feed_pk is None:
        return HttpResponseNotFound

    feed = get_object_or_404(FeedModel, pk=feed_pk)
    comments = CommentModel.objects.filter(feed_item__exact=feed).all()
    serializer = CommentSerializer(comments, many=True)
    return JsonResponse(serializer.data, safe=False)


class PostComment(CreateAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "feed_item"

    def create(self, request, *args, **kwargs):
        data = request.data
        data["type"] = CommentModel.Type.COMMENT
        if isinstance(request.user, AnonymousUser):
            data["anonymous"] = True
        else:
            data["user"] = request.user.pk
        data["feed_item"] = kwargs[self.lookup_field]
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


@csrf_exempt
@api_view(["POST"])
def post_comment(request, feed_pk):
    if feed_pk is None:
        return HttpResponseNotFound

    feed = get_object_or_404(FeedModel, pk=feed_pk)

    data = JSONParser().parse(request)
    data["feed_item"] = feed_pk

    user = request.user
    if type(user) == AnonymousUser:
        data["anonymous"] = True
    else:
        data["user"] = user.pk

    if "reply_to" in data:
        data["type"] = CommentModel.Type.ANSWER
    else:
        data["type"] = CommentModel.Type.COMMENT

    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            serializer.data, status=201, json_dumps_params={"ensure_ascii": False}
        )
    return JsonResponse(serializer.errors, status=400)
