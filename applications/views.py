from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from applications.models import ApplicationModel
from applications.serializers import ApplicationSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from clubs.models import ClubModel
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


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
