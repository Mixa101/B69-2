"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from posts.views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    UpdatePostView,
)
from user.views import register

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("register", register, name="register"),
    path("", PostListView.as_view(), name="post_list"),
    path("post/create/", PostCreateView.as_view(), name="create_post"),
    path("post/<int:pk>/edit", UpdatePostView.as_view(), name="edit_post"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="delete_post"),
    path("post/<int:id>", PostDetailView.as_view(), name="post_detail"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, dcoument_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
