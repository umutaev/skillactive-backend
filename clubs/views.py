from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from clubs.serializers import ClubSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from clubs.models import ClubModel
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ClubView(ListAPIView, CreateAPIView):
    queryset = ClubModel.objects.all()
    serializer_class = ClubSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        print(self.request.query_params)
        title = self.request.query_params.get("title", None)
        queryset = self.queryset
        if title is not None:
            searchable_title = "".join([i.lower() for i in title if i.isalpha()])
            queryset = queryset.filter(searchable_title__contains=searchable_title)
        min_price = self.request.query_params.get("min_price", None)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        max_price = self.request.query_params.get("max_price", None)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        age = self.request.query_params.get("age", None)
        if age is not None:
            queryset = queryset.filter(Q(min_age__lte=age) & Q(max_age__gte=age))
        gender = self.request.query_params.get("gender", None)
        if gender is not None:
            queryset = queryset.filter(
                Q(gender__exact=gender) | Q(gender__exact=ClubModel.Gender.BOTH)
            )
        owned = self.request.query_params.get("owned", None)
        if owned is not None and not isinstance(self.request.user, AnonymousUser):
            queryset = queryset.filter(author=self.request.user)
        elif not self.request.user.is_staff:
            queryset = queryset.filter(opened=True)
        return queryset.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data["author"] = request.user.pk
        data["searchable_title"] = "".join(
            [i.lower() for i in data.get("title", "") if i.isalpha()]
        )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SpecificClubView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = ClubModel.objects.all()
    serializer_class = ClubSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff and not self.get_object().author == request.user:
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff and not self.get_object().author == request.user:
            raise PermissionDenied
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff and not self.get_object().author == request.user:
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)


@csrf_exempt
@api_view(["POST"])
def post_club(request):
    data = JSONParser().parse(request)

    author = request.user
    if type(author) == AnonymousUser:
        raise PermissionDenied
    data["author"] = author.pk

    data["searchable_title"] = "".join(
        [i.lower() for i in data.get("title", "") if i.isalpha()]
    )

    serializer = ClubSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            serializer.data, status=201, json_dumps_params={"ensure_ascii": False}
        )
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET"])
def get_clubs_user(request):
    user = request.user
    if type(user) == AnonymousUser:
        raise PermissionDenied

    clubs = ClubModel.objects.filter(author__exact=user).all()
    serializer = ClubSerializer(clubs, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def club(request, pk):
    club = get_object_or_404(ClubModel, pk=pk)
    if request.method == "GET":
        serializer = ClubSerializer(club)
        return JsonResponse(serializer.data, safe=True)
    elif request.method == "PUT":
        if not (request.user.is_staff or club.author == request.user):
            raise PermissionDenied
        data = JSONParser().parse(request)
        serializer = ClubSerializer(club, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, json_dumps_params={"ensure_ascii": False}
            )
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        if not (request.user.is_staff or club.author == request.user):
            raise PermissionDenied
        club.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(["GET"])
def search_club(request):
    data = JSONParser().parse(request)
    clubs = ClubModel.objects

    if "title" in data:
        clubs = clubs.filter(
            searchable_title__contains="".join(
                [i.lower() for i in data["title"] if i.isalpha()]
            )
        )

    if "min_price" in data:
        clubs = clubs.filter(price__gte=data["min_price"])

    if "max_price" in data:
        clubs = clubs.filter(price__lte=data["max_price"])

    if "age" in data:
        clubs = clubs.filter(Q(min_age__lte=data["age"]) & Q(max_age__gte=data["age"]))

    if "gender" in data and data["gender"]:
        clubs = clubs.filter(
            Q(gender__exact=data["gender"]) | Q(gender__exact=ClubModel.Gender.BOTH)
        )

    # category and timetable filtration

    clubs = clubs.all()
    serializer = ClubSerializer(clubs, many=True)
    return JsonResponse(serializer.data, safe=False)
