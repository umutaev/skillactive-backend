from django.urls import path, include
from feed import views as feed_views
from comments import views as comments_views

urlpatterns = [
    path("", feed_views.FeedView.as_view()),
    path("<int:pk>", feed_views.FeedRecordView.as_view()),
    path("<int:feed_pk>/comments", feed_views.get_comments),
    path("<int:feed_pk>/comment", feed_views.post_comment),
]
