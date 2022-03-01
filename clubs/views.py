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
