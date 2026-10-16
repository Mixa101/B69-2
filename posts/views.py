from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from posts.forms import PostForm
from posts.models import Category, Post


# Create your views here.
def post_list(request: HttpRequest):
    posts = Post.objects.all()
    if search := request.GET.get("search"):
        posts = posts.filter(description__icontains=search)

    posts = posts.order_by("-created_at")
    return render(request, "posts/list.html", context={"posts": posts})


def post_detail(r, pk):
    post = Post.objects.get(id=pk)  # SELECT * FROM posts WHERE id = ?;
    return render(r, "posts/detail.html", context={"post": post})


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


@login_required
def delete_post(request: HttpRequest, pk):

    post = Post.objects.get(id=pk)

    if request.user != post.user:
        raise PermissionDenied

    if request.method.lower() == "post":
        post.delete()
        return redirect("post_list")

    return render(request, "posts/delete.html", context={"post": post})
