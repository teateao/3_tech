from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register',views.AccountCreateView.as_view(),name="register"),
    path('login',views.AccountLoginView.as_view(),name="login"),
    path('mypage',views.MypageApiView.as_view(),name="mypage"),
    path('article/main',views.ArticleApiView.as_view(),name="articles"),
    path('auth',views.Auth,name="auth"),
    path("article/<int:id>", views.EactArticleApiView.as_view(), name="article"),
]