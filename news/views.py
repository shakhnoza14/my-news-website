from django.shortcuts import render
from .models import CategoriaModel, NewsModel

def home_view(request):
    return render(request, 'index4.html')

def error_view (request):
    return render(request, '404.html')

def archive_view(request):
    return render(request, 'archive.html')

def author_view(request):
    return render(request, 'author.html')

def contact_view(request):
    return render(request, 'contact.html')

def gallery_view(request):
    return render(request, 'gallery.html')

def post_style_view(request):
    return render(request, 'post_style.html')

def single_news_view(request):
    return render(request, 'single_news.html')  