from datetime import datetime, timedelta

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives


from news.models import Category, Subscription

logger = logging.getLogger(__name__)

# наша задача по выводу текста на экран
def my_job():
    for category in Category.objects.all():  # перебираем категории

        # получаем email подписчиков по категориям
        subscribers = list(Subscription.objects.filter(category=category).values_list('user__email', flat=True))
        # получаем публикации по категориям за последне 7 дней
        posts = list(category.new_set.filter(date__gte=datetime.utcnow() - timedelta(days=7)))

        for email in subscribers:
            html_content = render_to_string(
                'daily_post.html',
                {
                    'link': settings.SITE_URL,
                    'posts_list': posts,
                }
            )

            msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email], )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


# функция, которая будет удалять неактуальные задачи
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику, для теста (second='*/10')
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),  # то же, что и интервал
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # каждую неделю будут удаляться старые задачи, которые не удалось выполнить или выполнять уже не надо
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")