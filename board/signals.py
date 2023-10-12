from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Reply




@receiver(post_save, sender=Reply)
def notify_response(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=f'Получен отклик на пост: "{instance.post.title}"',
            message=f'Отклик: "{instance.text}"',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.post.author.email],

    )