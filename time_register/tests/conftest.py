from ..models import Task

import pytest


@pytest.fixture
def blanket_task():
    return Task.objects.create(
        name='Task 1',
        begin='2023-03-01',
        end='2023-03-10',
        goal_daily_minutes=30,
    )


@pytest.fixture
def blanket_task2():
    return Task.objects.create(
        name='Task 2',
        begin='2023-03-11',
        end='2023-03-20',
        goal_daily_minutes=30,
    )
