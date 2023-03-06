from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from ..serializers import TaskSerializer, WorkEntrySerializer
from ..models import Task, WorkEntry

import pytest


@pytest.mark.django_db
def test_create_task(client):
    url = reverse("time_register:api:api_task-list")
    data = {
        "name": "Test Task",
        "begin": "2023-03-01",
        "end": "2023-03-10",
        "goal_daily_minutes": 60,
    }

    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the task was created
    task = Task.objects.get(name="Test Task")
    assert task.begin == date(2023, 3, 1)
    assert task.end == date(2023, 3, 10)
    assert task.goal_daily_minutes == 60


@pytest.mark.django_db
def test_allow_same_day_task(client):
    url = reverse("time_register:api:api_task-list")
    data = {
        "name": "Test Task",
        "begin": "2023-03-10",
        "end": "2023-03-10",
        "goal_daily_minutes": 60,
    }

    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_work_entry(client, blanket_task):
    data = {
        "begin": timezone.make_aware(datetime(2023, 3, 5, 12, 0, 0)),
        "end": timezone.make_aware(datetime(2023, 3, 5, 13, 0, 0)),
        "task": blanket_task.id,
    }
    url = reverse("time_register:api:api_work_entry-list")
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    work_entry = WorkEntry.objects.get(pk=1)
    assert work_entry.begin == data["begin"]
    assert work_entry.end == data["end"]
    assert work_entry.task == blanket_task


@pytest.mark.django_db
def acceptance_test_model_task():
    """
    Builder should stop `end` from being smaller than `begin`
    """
    task = Task.objects.create(
        name="Task 1",
        begin="2023-03-02",
        end="2023-03-01",
        goal_daily_minutes=30,
    )
    with pytest.raises(ValidationError):
        task.full_clean()


def acceptance_test_serializer_task(client):
    data = {
        "name": "Test Task",
        "begin": date(2023, 3, 5),
        "end": date(2023, 3, 4),
        "goal_daily_minutes": 60,
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()

    url = reverse("time_register:api_task")
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": ["Begin date must be before end date."]
    }


@pytest.mark.django_db
def acceptance_test_model_work_entry(blanket_task):
    """
    Builder should stop `end` from being smaller than `begin`
    """
    with pytest.raises(ValidationError):
        work_entry = WorkEntry(
            begin=datetime(2023, 3, 5, 12, 0, 0),
            end=datetime(2023, 3, 4, 10, 0, 0),
            task=blanket_task,
        )
        work_entry.full_clean()


@pytest.mark.django_db
def acceptance_test_serializer_work_entry(client, blanket_task):
    """
    Builder should stop `end` from being smaller than `begin`
    """
    data = {
        "begin": datetime(2023, 3, 5, 12, 0, 0),
        "end": datetime(2023, 3, 4, 10, 0, 0),
        "task": blanket_task.pk,
    }
    serializer = WorkEntrySerializer(data=data)
    assert not serializer.is_valid()

    url = reverse("time_register:api:api_work_entry-list")
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": ["End datetime must be after begin datetime."]
    }


@pytest.mark.django_db
def test_model_task_bigger_begin_than_end_raises_ValidationError():
    """
    Builder should stop `end` from being smaller than `begin`
    """
    task = Task.objects.create(
        name="Task 1",
        begin="2023-03-02",
        end="2023-03-01",
        goal_daily_minutes=30,
    )
    with pytest.raises(ValidationError):
        task.full_clean()


def test_serializer_task_bigger_begin_than_end_raises_ValidationError(client):
    data = {
        "name": "Test Task",
        "begin": date(2023, 3, 5),
        "end": date(2023, 3, 4),
        "goal_daily_minutes": 60,
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()

    url = reverse("time_register:api:api_task-list")
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": ["Begin date must be before end date."]
    }


@pytest.mark.django_db
def test_model_work_entry_bigger_begin_than_end_raises_ValidationError(blanket_task):
    """
    Builder should stop `end` from being smaller than `begin`
    """
    with pytest.raises(ValidationError):
        work_entry = WorkEntry(
            begin=datetime(2023, 3, 5, 12, 0, 0),
            end=datetime(2023, 3, 4, 10, 0, 0),
            task=blanket_task,
        )
        work_entry.full_clean()


@pytest.mark.django_db
def test_serializer_work_entry_bigger_begin_than_end_raises_ValidationError(
    client, blanket_task
):
    """
    Builder should stop `end` from being smaller than `begin`
    """
    data = {
        "begin": datetime(2023, 3, 5, 12, 0, 0),
        "end": datetime(2023, 3, 4, 10, 0, 0),
        "task": blanket_task.pk,
    }
    serializer = WorkEntrySerializer(data=data)
    assert not serializer.is_valid()

    url = reverse("time_register:api:api_work_entry-list")
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": ["End datetime must be after begin datetime."]
    }


@pytest.mark.django_db
def test_serializer_work_entry_outside_of_task_timespan_ValidationError(client):
    """
    Builder should stop workentry creation if not inside it's task timespan
    """
    task = Task.objects.create(
        name="Task 1",
        begin="2023-03-09",
        end="2023-03-10",
        goal_daily_minutes=30,
    )

    data1 = {
        "begin": datetime(2023, 3, 8, 23, 0, 0),
        "end": datetime(2023, 3, 9, 10, 0, 0),
        "task": task.pk,
    }
    serializer = WorkEntrySerializer(data=data1)
    assert not serializer.is_valid()

    url = reverse("time_register:api:api_work_entry-list")
    response = client.post(url, data1, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": [
            "Work Entry must be contained inside it's related task timespan."
        ]
    }

    data2 = {
        "begin": datetime(2023, 3, 9, 23, 0, 0),
        "end": datetime(2023, 3, 11, 10, 0, 0),
        "task": task.pk,
    }
    serializer = WorkEntrySerializer(data=data2)
    assert not serializer.is_valid()

    url = reverse("time_register:api:api_work_entry-list")
    response = client.post(url, data2, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": [
            "Work Entry must be contained inside it's related task timespan."
        ]
    }


@pytest.mark.django_db
def test_serializer_work_entry_violates_another_work_entry_raises_ValidationError(
    client, blanket_task
):
    data1 = {
        "begin": timezone.make_aware(datetime(2023, 3, 5, 12, 0, 0)),
        "end": timezone.make_aware(datetime(2023, 3, 5, 14, 0, 0)),
        "task": blanket_task.id,
    }
    url = reverse("time_register:api:api_work_entry-list")
    response = client.post(url, data1, format="json")

    data2 = {
        "begin": timezone.make_aware(datetime(2023, 3, 5, 13, 0, 0)),
        "end": timezone.make_aware(datetime(2023, 3, 5, 15, 0, 0)),
        "task": blanket_task.pk,
    }
    serializer = WorkEntrySerializer(data=data2)
    assert not serializer.is_valid()

    url = reverse("time_register:api:api_work_entry-list")
    response = client.post(url, data2, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "non_field_errors": [
            "Work Entry violates timespan of another Work Entry with id=1."
        ]
    }
