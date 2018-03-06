
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="author_info"),
    path('authors', views.author_general, name="author_general"),
    path('authors/<str:name>', views.author_about, name="author_info"),
    path('articles/<int:author_id>', views.author_articles,
         name="author_articles"),
    ]
