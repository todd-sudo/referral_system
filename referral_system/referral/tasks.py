import datetime
import random

from django_celery_beat.models import PeriodicTask

from config import celery_app
from referral_system.referral.utils import local_tz, utc_to_local


@celery_app.task(
    bind=True,
    name="referral.send_message_task",
    default_retry_delay=1 * 10,
    max_retries=30,
    soft_time_limit=60 * 30,
    time_limit=60 * 30,
)
def send_message_task(
        self,
        phone: str,
        code
):
    """ Таска для отправки сообщений пользователю (ИМИТАЦИЯ)
    """

    print(f"Код {code} отправлен на номер {phone}")
    return code


@celery_app.task(
    bind=True,
    name="referral.check_tasks_task",
    default_retry_delay=1 * 10,
    max_retries=30,
    soft_time_limit=60 * 30,
    time_limit=60 * 30,
)
def check_tasks_task(self):
    """ Таска, которая удаляет не нужные таски для рассылки
    """
    tasks = PeriodicTask.objects.all()
    date = datetime.datetime.now(local_tz)

    # for task in tasks:
    #     if task.expires is not None:
    #         task_expires = utc_to_local(task.expires)
    #         if date > task_expires:
    #             task.delete()

    tasks = PeriodicTask.objects.all()
    date = datetime.datetime.now(local_tz)

    for task in tasks:
        if task.enabled is False:
            task.delete()
