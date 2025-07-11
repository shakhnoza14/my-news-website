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


