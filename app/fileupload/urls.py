from fileupload.views import FileUploadView, MultipartFileUploadView
from django.urls import re_path

urlpatterns = [
    re_path(r"upload/(?P<filename>[^/]+)$", FileUploadView.as_view()),
    re_path(r"multipart/(?P<filename>[^/]+)$", MultipartFileUploadView.as_view()),
]
