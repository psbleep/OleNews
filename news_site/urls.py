from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('authors', views.author_general, name="author_general"),
    path('authors/<str:name>', views.author_about, name="author_info"),
    path('articles/<int:author_id>', views.author_articles,
         name="author_articles"),
    path('login/', auth_views.login, name="login"),
    path('signup/', views.sign_up, name="sign_up"),
    path('logout/', auth_views.logout, name="logout"),
]
