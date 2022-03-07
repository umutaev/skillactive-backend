from django.core.exceptions import PermissionDenied
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from categories.models import CategoryModel
from categories.serializers import CategorySerializer


class CategoriesView(ListAPIView, CreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().create(request, *args, **kwargs)


class CategoryView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
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
