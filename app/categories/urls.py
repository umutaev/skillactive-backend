from django.urls import path
from categories.views import CategoriesView, CategoryView

urlpatterns = [
    path("", CategoriesView.as_view()),
    path("<int:pk>/", CategoryView.as_view()),
]
