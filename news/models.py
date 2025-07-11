from django.db import models
from django.contrib.auth.models import User

class CategoriaModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class NewsModel(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField()
    video = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(CategoriaModel, on_delete=models.CASCADE)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'News table'
        verbose_name = 'News'
        verbose_name_plural = 'News'