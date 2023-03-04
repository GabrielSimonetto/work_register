from .models import Task, WorkEntry
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = []


class WorkEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEntry
        exclude = []
