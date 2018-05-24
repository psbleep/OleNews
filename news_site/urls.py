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
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(),
         name="article"),
    path('articles/<slug:slug>/like/', views.LikeArticleView.as_view(),
         name='like_article'),
    path('articles/<int:pk>/comment/', views.CreateCommentView.as_view(),
         name='comment_article'),
    path('users/<int:pk>/', views.UserProfileView.as_view(),
         name="user_profile"),
    path('users/<int:pk>/settings/', views.user_settings,
         name="user_profile_settings"),
    path('login/', auth_views.login, name="login"),
    path('signup/', views.UserSignupView.as_view(), name="sign_up"),
    path('logout/', auth_views.logout, name="logout"),
    path('change-password/', views.PasswordChangeView.as_view()),
    ]
