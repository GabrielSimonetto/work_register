from .models import Task, WorkEntry, GenericTest
from rest_framework import serializers


class GenericTestSerializer(serializers.ModelSerializer):
    resource = serializers.CharField(read_only=True)
    data = serializers.JSONField(read_only=True)

    class Meta:
        model = GenericTest
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = []

    def validate(self, data):
        if data["begin"] > data["end"]:
            raise serializers.ValidationError("Begin date must be before end date.")
        return data


class WorkEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEntry
        exclude = []

    def validate(self, data):
        begin = data["begin"]
        end = data["end"]

        # Check for begin precedence
        if begin >= end:
            raise serializers.ValidationError(
                "End datetime must be after begin datetime."
            )

        task = data["task"]

        # Check if work_entry timespan is inside it's task timespan
        if (task.begin > begin.date()) or (task.end < end.date()):
            raise serializers.ValidationError(
                "Work Entry must be contained inside it's related task timespan."
            )

        # Check if work_entry violates the timespan of another work_entry
        other_work_entries = WorkEntry.objects.filter(task=task)
        for other in other_work_entries:
            # candidate_begin must be after otherend or candidate_end before otherbegin
            # applying De Morgan:
            if (begin < other.end) and (end > other.begin):
                raise serializers.ValidationError(
                    f"Work Entry violates timespan of another Work Entry with id={other.id}."
                )

        return data
