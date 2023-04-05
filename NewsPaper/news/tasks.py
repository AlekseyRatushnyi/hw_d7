from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.celery import app

from .models import Post, Category
from .service import send


@app.task
def send_spam_email(user_email):
    send(user_email)