from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from apps.users.models import User
from django.template.loader import render_to_string
import os


@shared_task
def send_activate_account(user_id: int):
    user = User.objects.get(pk=user_id)
    subject = "Activar Cuenta"
    from_email = settings.EMAIL_HOST_USER
    web_server_host = settings.WEB_SERVER_HOST
    to_email = [user.email]
    html_content = render_to_string(
        "account_activate.html",
        {"web_server_host": web_server_host, "user": user, "token": user.pass_token},
    )
    msg = EmailMultiAlternatives(subject, "", from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_reset_email(user_id: int):
    user = User.objects.get(pk=user_id)
    subject = "Restablecimiento de Contraseña"
    from_email = settings.EMAIL_HOST_USER
    web_server_host = settings.WEB_SERVER_HOST
    to_email = [user.email]
    html_content = render_to_string(
        "reset_password.html",
        {"web_server_host": web_server_host, "user": user, "token": user.pass_token},
    )
    msg = EmailMultiAlternatives(subject, "", from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
