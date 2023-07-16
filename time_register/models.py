import datetime

from django.db import models
from django.core.exceptions import ValidationError


class GenericTest(models.Model):
    data = models.JSONField()
    resource = models.TextField()


class Task(models.Model):
    name = models.CharField(max_length=200)
    begin = models.DateField("begin date")
    end = models.DateField("end date")
    goal_daily_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    # TODO: perguntar sobre a existencia isso
    def clean(self):
        if self.begin > self.end:
            raise ValidationError("Begin date must be before end date.")

    def days_passed(self):
        # +1 in order to account for the current day
        return (datetime.date.today() - self.begin).days + 1

    @property
    def total_days(self):
        return (self.end - self.begin).days

    # TODO: perguntar sobre uso de properties em coisas que precisam acessar o banco
    def status(self):
        if self.time_worked() == self.desired_completed_time():
            return "On time"
        elif self.time_worked() > self.desired_completed_time():
            return "On surplus"
        elif self.time_worked() < self.desired_completed_time():
            return "On deficit"

        # TODO: raise error/logging stuff
        return "Unexpected Result"

    def differential_time(self):
        return self.time_worked() - self.desired_completed_time()

    def display_differential_time(self):
        return abs(self.differential_time())

    def time_worked(self):
        return sum(
            [work_entry.time_worked for work_entry in self.workentry_set.all()],
            start=datetime.timedelta(),
        )

    def desired_completed_time(self):
        return datetime.timedelta(minutes=self.days_passed() * self.goal_daily_minutes)


class WorkEntry(models.Model):
    begin = models.DateTimeField("begin work")
    end = models.DateTimeField("end work")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        if self.begin.date() == self.end.date():
            output = f"""{self.begin.strftime(" %d/%m/%Y: %Hh%M")} - {self.end.strftime(" %Hh%M")}"""
            return output

        return f"""{self.begin.strftime(" %d/%m/%Y: %Hh%M")} - {self.end.strftime(" %Hh%M - - %d/%m/%Y")}"""

    # TODO: perguntar sobre a existencia isso
    def clean(self):
        if self.begin > self.end:
            raise ValidationError("End datetime must be after begin datetime.")

    def __iter__(self):
        return iter((self.begin, self.end))

    @property
    def time_worked(self):
        return self.end - self.begin
