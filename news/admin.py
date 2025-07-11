from django.contrib import admin
from .models import CategoriaModel, NewsModel

@admin.register(CategoriaModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    list_display_links = ('name',)

@admin.register(NewsModel)
class NewsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'created_at',)
    search_fields = ('name', 'text',)
    list_filter = ('created_at',)
    list_per_page = 10
    list_display_links = ('text', 'name',)
    prepopulated_fields = {'slug': ('name',)}
