from django.urls import path
from comments.views import comment, post_comment

urlpatterns = [path("<int:pk>/", comment), path("<int:pk>/reply", post_comment)]
