from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def send_welcome_email(user):
    subject = 'Welcome to YourSite'
    message = f'Hello, {user.username}! Thank you for registering on YourSite.'
    from_email = 'your-email@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

@receiver(post_save, sender=User)
def send_welcome_email_on_register(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance)
