from django.views.decorators.csrf import csrf_exempt
from feed import serializers
from feed.models import FeedModel
from feed.serializers import FeedSerialier
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import PermissionDenied

@csrf_exempt
@api_view(['GET', 'POST'])
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
            return JsonResponse(serializer.data, status=201, json_dumps_params={"ensure_ascii": False})
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
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
            return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == "DELETE":
        if not request.user.is_staff:
            raise PermissionDenied
        feed_object.delete()
        return HttpResponse(status=204)
