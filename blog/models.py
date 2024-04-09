from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    name_es = models.CharField(
        max_length=30, verbose_name=_("Name (Spanish)"), blank=True, null=True
    )

    class Meta:
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    # Translation admin title and body
    title_es = models.CharField(
        max_length=255, verbose_name=_("Title (Spanish)"), blank=True, null=True
    )
    body_es = models.TextField(verbose_name=_("Body (Spanish)"), blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    image = models.ImageField(
        upload_to="featured_image/%Y/%m/%d/", blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
