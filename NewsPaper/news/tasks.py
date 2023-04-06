from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from NewsPaper.celery import app
from django.utils import timezone

from .models import Post, Category



@shared_task
def notify_subscribers_weekly():
    template = "daily_post.html"
    email_subject = 'Еженедельный дайджест для подписчиков категории'
    time_delta = datetime.now(tz=timezone.get_current_timezone()) - timedelta(days=7)
    past_week_posts = Post.objects.filter(time_create__gte=time_delta)
    past_week_categories = set(past_week_posts.values_list('category__name', flat=True))

    subscribers = set(Category.objects.filter(name__in=past_week_categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
            template,
            {
                'posts': past_week_posts,
                'categories': past_week_categories,
            }
        )

    msg = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def new_post_subscription(pk):
    post = Post.objects.get(pk=pk)
    subscribers = post.category.values(
        'subscribers__email', 'subscribers__username'
    )
    cat = post.category.values('name')[0]['name']
    for subscriber in subscribers:
        html_content = render_to_string(
            'post_created_email.html',
            {
                'post': post,
                'username': subscriber.get("subscribers__username"),
                'post_url': post.get_absolute_url(),
                'cat':cat,
            }
        )
        msg = EmailMultiAlternatives(
            subject=post.title,
            body=post.text_post,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.get("subscribers__email")],
            )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

