from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import FileSystemStorage
from uuid import uuid4


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.FILES["file"]
        uuid_string = uuid4().hex
        fss = FileSystemStorage()
        file = fss.save(uuid_string + "_" + filename, file_obj)
        file_url = fss.url(file)
        return Response(status=201, data={"path": file_url})
