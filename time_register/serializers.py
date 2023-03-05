from .models import Task, WorkEntry
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = []

    def validate(self, data):
        if data['begin'] > data['end']:
            raise serializers.ValidationError(
                'Begin date must be before end date.')
        return data


class WorkEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEntry
        exclude = []

    def validate(self, data):
        if data['begin'] > data['end']:
            raise serializers.ValidationError(
                'Begin datetime must be before end datetime.')
        return data
