from django.db import models
from django.contrib.auth.models import User

class Usermodel(User):
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'

class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"
    
    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'ContactModel'
        verbose_name_plural = 'ContactModels'
        ordering = ['-created_at']


class ProfileModel(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')
    banner = models.ImageField(upload_to='profile_banners/', default='profile_banners/default_banner.jpg')

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'ProfileModel'
        verbose_name_plural = 'ProfileModels'


