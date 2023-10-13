from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from unicodedata import category
from news.models import Category, Subscription

@shared_task
def with_every_new_post(category, preview, title, emails, get_absolute_url):

    subject = f'Новая запись в категории {category}'

    text_content = (
        f'Название: {title}\n'
        f'Анонс: {preview}\n\n'
        f'Ссылка на публикацию: {settings.SITE_URL}{get_absolute_url}'
    )
    html_content = (
        f'Название: {title}<br>'
        f'Анонс: {preview}<br><br>'
        f'<a href="{settings.SITE_URL}{get_absolute_url}">'
        f'Ссылка на публикацию</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_newsletter():
    for cat in Category.objects.all():

        subscribers = list(Subscription.objects.filter(category=cat).values_list('user__email', flat=True))

        posts_list = list(cat.record_set.filter(data__gte=datetime.utcnow() - timedelta(days=7)))

        if len(posts_list) == 0:
            break

        for email in subscribers:
            html_content = render_to_string(
                'daily_post.html',
                {
                    'link': settings.SITE_URL,
                    'posts_list': posts_list,
                }
            )

            msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email], )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()