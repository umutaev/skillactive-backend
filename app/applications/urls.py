from django.urls import path
from applications.views import ApplicationView

urlpatterns = [path("<int:pk>/", ApplicationView.as_view())]
