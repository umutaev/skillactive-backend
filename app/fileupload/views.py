from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from django.utils.datastructures import MultiValueDictKeyError


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.FILES["file"]
        uuid_string = uuid4().hex
        fss = FileSystemStorage()
        file = fss.save(uuid_string + "_" + filename, file_obj)
        file_url = fss.url(file)
        return Response(status=201, data={"path": file_url})


class MultipartFileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def put(self, request, filename, format=None):
        try:
            file_obj = request.data["media"]
        except MultiValueDictKeyError:
            return Response(
                status=400, data={"error": 'file should be in the "media" field'}
            )
        uuid_string = uuid4().hex
        fss = FileSystemStorage()
        file = fss.save(uuid_string + "_" + filename, file_obj)
        file_url = fss.url(file)
        return Response(status=201, data={"path": file_url})
