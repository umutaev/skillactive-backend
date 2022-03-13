from fileupload.views import FileUploadView
from django.urls import re_path

urlpatterns = [re_path(r"upload/(?P<filename>[^/]+)$", FileUploadView.as_view())]
