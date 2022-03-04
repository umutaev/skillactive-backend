from django.urls import path
from applications.views import ApplicationsView

urlpatterns = [path("", ApplicationsView.as_view())]
