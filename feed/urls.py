from django.urls import path, include
from feed import views as feed_views
from comments import views as comments_views

urlpatterns = [
    path("", feed_views.feed_list),
    path("<int:pk>", feed_views.feed_detail),
    path("<int:feed_pk>/comments", feed_views.get_comments),
    path("<int:feed_pk>/comment", feed_views.post_comment),
]
