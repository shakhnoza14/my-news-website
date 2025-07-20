# yourapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Usermodel, ProfileModel


@receiver(post_save, sender=Usermodel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
        subject = 'Welcome to News Site!'
        message = f'Hi {instance.username},\n\nThanks for registering at News Site. We’re happy to have you here!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
