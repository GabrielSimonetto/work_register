from datetime import date, datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import TaskSerializer, WorkEntrySerializer
from .models import Task, WorkEntry

import pytest


@pytest.fixture
def blanket_task():
    return Task.objects.create(
        name='Task 1',
        begin='2023-03-01',
        end='2023-03-10',
        goal_daily_minutes=30,
    )


class TaskModelTests(TestCase):
    def test_bigger_begin_than_end_raises_ValidationError(self):
        """
        Builder should stop `end` from being smaller than `begin`
        """
        with self.assertRaises(ValidationError):
            task = Task(name='Test Task', begin=date(2023, 1, 2),
                        end=date(2023, 1, 1), goal_daily_minutes=60)
            task.full_clean()


class TaskSerializerTests(APITestCase):
    def test_bigger_begin_than_end_raises_ValidationError(self):
        data = {
            'name': 'Test Task',
            'begin': date(2023, 3, 5),
            'end': date(2023, 3, 4),
            'goal_daily_minutes': 60
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        url = reverse('time_register:api_task')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [
                         'Begin date must be before end date.']})


class WorkEntryModelTests(TestCase):
    def test_bigger_begin_than_end_raises_ValidationError(self, blanket_task):
        """
        Builder should stop `end` from being smaller than `begin`
        """
        with self.assertRaises(ValidationError):
            work_entry = WorkEntry(begin=datetime(2023, 3, 5, 12, 0, 0),
                                   end=datetime(2023, 3, 4, 10, 0, 0), task=blanket_task.pk)
            work_entry.full_clean()


class WorkEntrySerializerTests(APITestCase):
    def test_bigger_begin_than_end_raises_ValidationError(self, blanket_task):
        data = {
            'begin': datetime(2023, 3, 5, 12, 0, 0),
            'end': datetime(2023, 3, 4, 10, 0, 0),
            'task': blanket_task.pk,
        }
        serializer = WorkEntrySerializer(data=data)
        self.assertFalse(serializer.is_valid())

        url = reverse('time_register:api_work_entry')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [
                         'Begin datetime must be before end datetime.']})
