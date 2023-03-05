import datetime

from django.db import models
from django.core.exceptions import ValidationError

# TODO: Feature: different ways to insert goal
#   goal_weekly, total_goal
# TODO: Feature: session based goals
#   and no_goal (currently implicit if goal is none)


class Task(models.Model):
    name = models.CharField(max_length=200)
    begin = models.DateField('begin date')
    end = models.DateField('end date')
    goal_daily_minutes = models.PositiveIntegerField()

    # pub_date = models.DateTimeField('pub date')
    # TODO: allow none (task without a goal, and with no need for begin and end dates)
    #       either they all are required, or none of them are?
    #       and then it makes it somewhat troublesome to display stuff? maybe

    # TODO: don't allow more than 24h of a goal per day

    def __str__(self):
        return self.name

    def clean(self):
        if self.begin > self.end:
            raise ValidationError('Begin date must be before end date.')

    def days_passed(self):
        # +1 in order to account for the current day
        return (datetime.date.today() - self.begin).days + 1

    def total_days(self):
        return (self.end - self.begin).days

    # TODO: check for property here
    #    idk how much it saves on processing but at least code gets prettier
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

    # TODO: it would be useful if i always could return a smart
    #   time differential object
    #   which prints itself as the minimum of hours and minutes
    #   (instead of like: 135 minutes)
    #   well i guess datetime already does this somewhat
    #   just need to check.
    #
    # the problem with this is i will need to have
    # both the function with the value, and the one that formats it
    # because i will not be checking formatting on the templates.

    def time_worked(self):
        # TODO: Actually implement this.
        # import datetime
        # return datetime.timedelta(seconds=10800)

        return sum([work_entry.time_worked() for work_entry in self.workentry_set.all()], start=datetime.timedelta())

    def desired_completed_time(self):
        return datetime.timedelta(minutes=self.days_passed() * self.goal_daily_minutes)


class WorkEntry(models.Model):
    begin = models.DateTimeField('begin work')
    end = models.DateTimeField('end work')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    # TODO deny end datetimes that come before begin datetimes

    def __str__(self):
        # TODO: Format to have only hours and minutes
        # TODO: Format to have only hours and minutes
        # TODO: for the love of god clean this
        # TODO: how to test for equal, day, month, year?
        #           self.begin.date == self.begin.date ??
        if self.begin.date() == self.end.date():
            output = f"""{self.begin.strftime(" %d/%m/%Y: %Hh%M")} - {self.end.strftime(" %Hh%M")}"""
            return output

        return f"""{self.begin.strftime(" %d/%m/%Y: %Hh%M")} - {self.end.strftime(" %Hh%M - - %d/%m/%Y")}"""

    def clean(self):
        if self.begin > self.end:
            raise ValidationError(
                'Begin datetime must be before end datetime.')

    def __iter__(self):
        return iter((self.begin, self.end))

    def time_worked(self):
        return self.end - self.begin
