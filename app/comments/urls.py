from django.urls import path
from comments.views import SpecificCommentView, CommentView, LikeRequest

urlpatterns = [
    path("", CommentView.as_view(), name="Comment"),
    path("<int:pk>/", SpecificCommentView.as_view()),
    path("<int:pk>/like", LikeRequest.as_view()),
]
