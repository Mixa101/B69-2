from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from posts.forms import PostForm
from posts.models import Category, Post


# Create your views here.
def post_list(request: HttpRequest):
    posts = Post.objects.all()
    if search := request.GET.get("search"):
        posts = posts.filter(description__icontains=search)
    return render(request, "posts/list.html", context={"posts": posts})


def post_detail(r, pk):
    post = Post.objects.get(id=pk)  # SELECT * FROM posts WHERE id = ?;
    return render(r, "posts/detail.html", context={"post": post})


def create_post(request: HttpRequest):

    if request.method.lower() == "post":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("post_detail", form.instance.pk)

    categories = Category.objects.all()
    return render(request, "posts/create.html", {"categories": categories})
