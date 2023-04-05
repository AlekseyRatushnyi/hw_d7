from django.core.mail import send_mail
from django.conf import settings

from .models import Category


def send(user_email):
        subject = "Тема"
        message = "Текстовка"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,)

