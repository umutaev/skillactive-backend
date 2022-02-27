from django.views.decorators.csrf import csrf_exempt
from comments.models import CommentModel
from feed.models import FeedModel
from comments.serializers import CommentSerializer
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
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
            return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})
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
@api_view(['POST'])
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
        return JsonResponse(serializer.data, status=201, json_dumps_params={"ensure_ascii": False})
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def modify(request, pk):
    if request.method == "PUT":
        comment = get_object_or_404(CommentModel, pk=pk)
        if not (request.user.is_staff or comment.user == request.user):
            raise PermissionDenied
        data = JSONParser().parse(request)
        serializer = CommentModel(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})
        return JsonResponse(serializer.errors, status=400)



"""@csrf_exempt
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
"""