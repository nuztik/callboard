import logging
import datetime

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.models import User
from django.utils import timezone

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail

from callboard.board.models import Post
from callboard.callboard.settings import SITE_URL

logger = logging.getLogger(__name__)

def send_weekly_email():
    last_week = timezone.now() - timezone.timedelta(days=7)
    weekly_posts = Post.objects.filter(created__gte=last_week)
    if weekly_posts:
        recipients = []
        msg = '\n'
        for post in weekly_posts:
            msg += f'"{post.title}" опубликован: {str(post.created)[:19]}\n'

        users = User.objects.all()
        for user in users:
            recipients.append(user.email)
        send_mail(
            subject=f'Новые посты за неделю.',
            message=f'Опубликованы следующие посты: {msg}\nПодробнее на {SITE_URL}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
        )





def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_email,
            trigger=CronTrigger(day_of_week="sun", hour="23", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="send_weekly_email",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_email'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")