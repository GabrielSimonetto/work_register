import datetime

import pytest
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..models import Task


@pytest.mark.django_db
def test_no_tasks(client):
    """
        If no tasks exist, an appropriate message is displayed.
        """
    response = client.get(reverse('time_register:index'))

    assert response.status_code == 200
    assert "No tasks are available." in response.content.decode()
    assert list(response.context['latest_task_list']) == []


@pytest.mark.django_db
def test_one_task_is_displayed(client, blanket_task):
    """
    Test that one inserted task will be displayed on the page.
    """
    blanket_task.save()

    response = client.get(reverse('time_register:index'))
    assert list(response.context['latest_task_list']) == [blanket_task]


@pytest.mark.django_db
def test_many_tasks_are_displayed(client, blanket_task, blanket_task2):
    """
    Test that one inserted task will be displayed on the page.
    """
    blanket_task.save()
    blanket_task2.save()

    response = client.get(reverse('time_register:index'))
    assert list(response.context['latest_task_list']) == [
        blanket_task, blanket_task2]


@pytest.mark.django_db
def test_inexistent_detail_page(client):
    """
    The detail view of a question with a pub_date in the future
    returns a 404 not found.
    """
    url = reverse('time_register:detail', args=(999,))
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_found_detail_page(client, blanket_task):
    """
    The detail view of a question with a pub_date in the future
    returns a 404 not found.
    """
    blanket_task.save()
    url = reverse('time_register:detail', args=(1,))
    response = client.get(url)

    content = response.content.decode()

    assert response.status_code == 200
    assert 'Task 1' in content
    assert 'Task timeframe: March 1, 2023 -- March 10, 2023' in content
    assert 'Daily Goal: 30 minutes' in content
