import json
from typing import Union

import pytz as pytz
from django_celery_beat.models import PeriodicTask, IntervalSchedule


def create_task_message_send(
        name_task: str,
        phone: str,
        code: Union[str, int],
        start_time,
):
    """ Создает таски для отправки сообщений
    """
    schedule, created_interval = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.SECONDS,
    )
    task: PeriodicTask = PeriodicTask.objects.create(
        interval=schedule,
        name=name_task,
        start_time=start_time,
        task="referral.send_message_task",
        kwargs=json.dumps({"phone": phone, "code": code}),
        one_off=True
    )
    return task


local_tz = pytz.timezone('Europe/Moscow')


def utc_to_local(utc_dt):
    """ Преобразует UTC в Europe/Moscow
    """
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

