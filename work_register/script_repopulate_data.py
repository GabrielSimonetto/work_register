from time_register.models import *
from django.utils import timezone

now = timezone.now()
t = Task(task_name="TCC", pub_date=now)

t.save()

t.workentry_set.create(
    begin=timezone.datetime(2023, 2, 6, 11, 0, 0),
    end=timezone.datetime(2023, 2, 6, 12, 0, 0), 
)

t.workentry_set.create(
    begin=timezone.datetime(2023, 2, 7, 11, 15, 0),
    end=timezone.datetime(2023, 2, 7, 13, 0, 0), 
)