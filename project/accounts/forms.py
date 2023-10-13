from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm
from django.core.mail import send_mail, mail_managers, mail_admins

from django.core.mail import EmailMultiAlternatives


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)  # вызываем этот же метод класса-родителя, чтобы необходимые проверки и сохранение в модель User были выполнены.

        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, Вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, Вы успешно зарегистрировались на сайте '
            f'<a href="http://127.0.0.1:8000/"> NEW autoBASS</a>!'
        )

        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )

        msg.attach_alternative(html, "text/html")
        msg.send()

        # при новых регистрациях, всем менеджерам из настроек проекта будет отправлено оповещение
        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        # при новой регистрации, всем администраторам из настроек проекта будет приходить оповещение
        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user


    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

