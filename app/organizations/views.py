from urllib import request
from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from organizations.serializers import OrganizationSerializer
from organizations.models import OrganizationModel
from rest_framework import status


class OrganizationsView(ListAPIView, CreateAPIView):
    queryset = OrganizationModel.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().list(request, *args, **kwargs)


class OrganizationView(RetrieveAPIView, UpdateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    queryset = OrganizationModel.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        object = queryset.get(owner=self.request.user)
        return object
