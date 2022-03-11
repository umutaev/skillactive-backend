from django.urls import path, include
from feed.views import FeedView, FeedRecordView, PostComment, ViewRequest, LikeRequest
from feed import views as feed_views


urlpatterns = [
    path("", FeedView.as_view()),
    path("<int:pk>", FeedRecordView.as_view()),
    path("<int:pk>/view", ViewRequest.as_view()),
    path("<int:pk>/like", LikeRequest.as_view()),
    path("<int:feed_item>/comment", PostComment.as_view()),
    # path("<int:feed_item>/comment", feed_views.post_comment),
]
