from django.db import models


class Category(models.Model):
    title = models.CharField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField()
    image = models.ImageField(null=True, upload_to="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
