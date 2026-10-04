from django.http.request import HttpRequest
from django.shortcuts import render

from posts.models import Post


# Create your views here.
def post_list(request: HttpRequest):
    posts = Post.objects.all()  # SELECT * FROM posts;
    print(request.path)
    return render(request, "posts/list.html", context={"posts": posts})


def post_detail(r, pk):
    post = Post.objects.get(id=pk)  # SELECT * FROM posts WHERE id = ?;
    print(r.path)
    return render(r, "posts/detail.html", context={"post": post})
