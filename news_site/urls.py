from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('authors/', views.AuthorsListView.as_view(), name="authors_list"),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name="author"),
    path('authors/<int:pk>/articles/', views.AuthorArticlesView.as_view(),
         name="author_articles"),
    path('articles/', views.ArticlesListView.as_view(), name="articles_list"),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(),
         name="article"),
    path('login/', views.log_in, name="login"),
    path('user/settings', views.user_settings, name='like'),
    path('user/<str:user_name>', views.user_profile, name="user_page"),
    path('signup/', views.sign_up, name="sign_up"),
    path('logout/', auth_views.logout, name="logout"),
    path('comment_submit/', views.comment_submit, name="comment_submit"),
    path('like/', views.like, name='like'),
]
