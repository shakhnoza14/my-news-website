from django.urls import path
from .views import home_view, error_view, archive_view, author_view, contact_view, gallery_view, post_style_view, single_news_view

urlpatterns = [
    path('', home_view, name='home'),
    path('404/', error_view, name='error'),
    path('archive/', archive_view, name='archive'),
    path('author/', author_view, name='author'),
    path('contact/', contact_view, name='contact'),
    path('gallery/', gallery_view, name='gallery'),
    path('post_style/', post_style_view, name='post_style'),
    path('news/<slug:slug>/', single_news_view, name='single_news'),
]
