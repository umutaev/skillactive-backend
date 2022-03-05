from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from applications.models import ApplicationModel
from applications.serializers import ApplicationSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from clubs.models import ClubModel
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class ApplicationsView(ListAPIView, CreateAPIView):
    queryset = ApplicationModel.objects.all()
    serializer_class = ApplicationSerializer
    lookup_field = "club"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(club=kwargs["club"]).all()
        if (
            not queryset.first().club.author == request.user
            and not request.user.is_staff
        ):
            raise PermissionDenied

        """page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)"""

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        data["club"] = kwargs["club"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ApplicationView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = ApplicationModel.objects.all()
    serializer_class = ApplicationSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        if (
            not self.get_object().club.author == request.user
            and not request.user.is_staff
        ):
            raise PermissionDenied
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if (
            not self.get_object().club.author == request.user
            and not request.user.is_staff
        ):
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if (
            not self.get_object().club.author == request.user
            and not request.user.is_staff
        ):
            raise PermissionDenied
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if (
            not self.get_object().club.author == request.user
            and not request.user.is_staff
        ):
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)


@csrf_exempt
@api_view(["POST", "GET"])
def applications(request, pk):
    club = get_object_or_404(ClubModel, pk=pk)
    if request.method == "GET":
        user = request.user
        if not club.author == user and not user.is_staff:
            raise PermissionDenied
        applications_list = ApplicationModel.objects.filter(club__exact=club)
        serializer = ApplicationSerializer(applications_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        data["club"] = club.pk
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, status=201, json_dumps_params={"ensure_ascii": False}
            )
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def application(request, pk_club, pk_application):
    club = get_object_or_404(ClubModel, pk=pk_club)
    application = get_object_or_404(ApplicationModel, pk=pk_application)
    user = request.user
    if not club.author == user and not user.is_staff:
        raise PermissionDenied
    if not application.club == club:
        return HttpResponse(status=400)
    if request.method == "GET":
        serializer = ApplicationSerializer(application)
        return JsonResponse(serializer.data, safe=True)
    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ApplicationSerializer(application, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, json_dumps_params={"ensure_ascii": False}
            )
        return JsonResponse(serializer.errors, status=400)
    if request.method == "DELETE":
        application.delete()
        return HttpResponse(status=204)
