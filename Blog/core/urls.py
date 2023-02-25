from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register',views.AccountCreateView.as_view(),name="register"),
    path('login',views.AccountLoginView.as_view(),name="login"),
    path('article/main',views.ArticleApiView.as_view(),name="articles"),
]