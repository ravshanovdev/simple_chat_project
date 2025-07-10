from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verification_email(email, code):
    send_mail(
        'code sent.!',
        f"CODE: {code}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
