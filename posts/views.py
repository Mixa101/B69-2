from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from posts.forms import PostForm
from posts.models import Category, Post
from posts.services import get_by_filter


# Create your views here.
def post_list(request: HttpRequest):

    # работа с БД
    posts = Post.objects.all()
    if search := request.GET.get("search"):
        posts = posts.filter(description__icontains=search)

    posts = posts.order_by("-created_at")
    # работа с контекстом и HTMl
    return render(request, "posts/list.html", context={"posts": posts})


class PostListView(ListView):
    model = Post
    template_name = "posts/list.html"
    context_object_name = "posts"

    # Для работы с базой данных
    def get_queryset(self) -> QuerySet[Any, Any]:
        queryset = super().get_queryset()
        search = self.request.GET.get("search")

        return get_by_filter(queryset, search=search, name="islam")


def post_detail(r, pk):
    post = Post.objects.get(id=pk)  # SELECT * FROM posts WHERE id = ?;
    return render(r, "posts/detail.html", context={"post": post})


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/detail.html"
    pk_url_kwarg = "id"


@login_required
def create_post(request: HttpRequest):

    if request.method.lower() == "post":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("post_detail", form.instance.pk)

    categories = Category.objects.all()
    return render(request, "posts/create.html", {"categories": categories})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy("post_list")
    template_name = "posts/create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context


@login_required
def edit_post(request: HttpRequest, pk):
    post = Post.objects.get(id=pk)

    if post.user != request.user:
        raise PermissionDenied

    if request.method.lower() == "post":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=form.instance.id)
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit.html", context={"form": form})


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/edit.html"

    def get_object(self, queryset: QuerySet[Any, Any] | None = None) -> Model:
        post = super().get_object(queryset)
        if self.request.user != post.user:
            raise PermissionDenied()
        return post


@login_required
def delete_post(request: HttpRequest, pk):

    post = Post.objects.get(id=pk)

    if request.user != post.user:
        raise PermissionDenied

    if request.method.lower() == "post":
        post.delete()
        return redirect("post_list")

    return render(request, "posts/delete.html", context={"post": post})


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/delete.html"
    success_url = reverse_lazy("post_list")
