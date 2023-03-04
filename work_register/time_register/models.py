from django.db import models


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # TODO Task begin date, not pub date.

    def __str__(self):
        return self.task_name


class WorkEntry(models.Model):
    begin = models.DateTimeField('begin work')
    end = models.DateTimeField('end work')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        # TODO: Format to have only hours and minutes
        return f"{self.begin} - {self.end}"
