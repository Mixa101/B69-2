from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from posts.models import Post


# Create your views here.
def post_list(request: HttpRequest):
    posts = Post.objects.all()
    if search := request.GET.get("search"):
        posts = posts.filter(description__icontains=search)
    return render(request, "posts/list.html", context={"posts": posts})


def post_detail(r, pk):
    post = Post.objects.get(id=pk)  # SELECT * FROM posts WHERE id = ?;
    print(r.path)
    return render(r, "posts/detail.html", context={"post": post})


def create_post(request: HttpRequest):

    if request.method.lower() == "post":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        post = Post.objects.create(title=title, description=description, image=image)

        return redirect("post_detail", post.pk)

    return render(request, "posts/create.html")
