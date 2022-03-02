from django.urls import path
from comments.views import comment, post_comment, CommentView

urlpatterns = [
    path("<int:pk>/", comment),
    path("<int:pk>/class_based", CommentView.as_view(), name="Comment"),
    path("<int:pk>/reply", post_comment),
]
