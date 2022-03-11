from django.core.exceptions import PermissionDenied
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from districts.models import DistrictModel
from districts.serializers import DistrictSerializer


class DistricsView(ListAPIView, CreateAPIView):
    queryset = DistrictModel.objects.all()
    serializer_class = DistrictSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        q = super().get_queryset()
        q = q.filter(deleted=False)
        return q

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().create(request, *args, **kwargs)


class DistricView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = DistrictModel.objects.all()
    serializer_class = DistrictSerializer
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

        instance = self.get_object()
        instance.deleted = True
        instance.save()

        return super().retrieve(request, *args, **kwargs)
