from django.urls import path
from feed import views

urlpatterns = [
    path('', views.feed_list),
    path('<int:pk>', views.feed_detail)
]