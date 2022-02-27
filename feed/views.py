from django.views.decorators.csrf import csrf_exempt
from feed.models import FeedModel
from feed.serializers import FeedSerialier
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from comments.models import CommentModel
from comments.serializers import CommentSerializer

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

@csrf_exempt
@api_view(['GET'])
def get_comments(request, feed_pk):
    if feed_pk is None:
        return HttpResponseNotFound
    
    feed = get_object_or_404(FeedModel, pk=feed_pk)
    comments = CommentModel.objects.filter(feed_item__exact=feed).all()
    serializer = CommentSerializer(comments, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['POST'])
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
        return JsonResponse(serializer.data, status=201, json_dumps_params={"ensure_ascii": False})
    return JsonResponse(serializer.errors, status=400)
