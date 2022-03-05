from django.urls import path
from comments.views import comment, post_comment, CommentView

urlpatterns = [path("<int:pk>/", CommentView.as_view(), name="Comment")]
