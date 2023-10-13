from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from .tasks import *

from .models import New


@receiver(post_save, sender=New)  # декоратор для сигналов
def New_created(sender, instance, created, **kwargs):
    print('Создан товар', instance)

    if created:  # при появлении новой публикации
        # получаем email подписчиков этой публикации
        emails = list(User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True))

        # вызываем нашу таску и передаем ей необходимые аргументы
        with_every_new_post.delay(instance.category.title,
                                  instance.preview(),
                                  instance.title,
                                  emails,
                                  instance.get_absolute_url(),
                                  )


#@receiver(post_save, sender=New)
#def New_created(instance, sender, created, **kwargs):
#    print('Создан товар', instance)
#    if created:
#        emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)

#        subject = f'Новая запись в категории {instance.category}'

#        text_content = (
#            f'Название: {instance.title}\n'
#            f'Анонс: {instance.preview()}\n\n'
#            f'Ссылка на публикацию: {settings.SITE_URL}{instance.get_absolute_url()}'
#        )
#        html_content = (
#            f'Название: {instance.title}<br>'
#            f'Анонс: {instance.preview()}<br><br>'
#            f'<a href="{settings.SITE_URL}{instance.get_absolute_url()}">'
#            f'Ссылка на публикацию</a>'
#        )
#        for email in emails:
#            msg = EmailMultiAlternatives(subject, text_content, None, [email])
#            msg.attach_alternative(html_content, "text/html")
#            msg.send()