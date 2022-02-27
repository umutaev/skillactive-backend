from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/', include('feed.urls')),
    path('users/', include('users.urls')),
    path('comments/', include('comments.urls'))
]
