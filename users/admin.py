from django.contrib import admin
from .models import ContactModel, Usermodel, ProfileModel
@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    list_per_page = 10
    list_display_links = ('email', 'name')

@admin.register(Usermodel)
class UsermodelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth')
    search_fields = ('username', 'email')
    list_filter = ('date_of_birth',)
    list_per_page = 10
    list_display_links = ('username', 'email')

@admin.register(ProfileModel)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'banner')
    search_fields = ('user__username',)
    list_filter = ('user__date_joined',)
    list_per_page = 10
    list_display_links = ('user',)