from django.contrib import admin

from .models import Task, WorkEntry

admin.site.register(Task)
admin.site.register(WorkEntry)
