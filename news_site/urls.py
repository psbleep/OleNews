from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('authors', views.author_general, name="author_general"),
    path('authors/<int:author_id>', views.author_about, name="author_info"),
    path('authors/<int:author_id>/<str:article>', views.author_article_show, name="author_article_show"),
    path('articles/', views.articles_main, name="articles_main"),
    path('articles/<int:author_id>', views.author_articles,
         name="author_articles"),
    path('login/', views.log_in, name="login"),
    path('user/', views.user_profile, name="user_page"),
    path('signup/', views.sign_up, name="sign_up"),
    path('logout/', auth_views.logout, name="logout"),
    path('comment_submit/', views.comment_submit, name="comment_submit"),
]
