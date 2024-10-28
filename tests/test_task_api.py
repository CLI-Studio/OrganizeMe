import os
import json
import pytest
from typing import Dict
from organize_me.task_api import TaskApi
from organize_me.task import Task
from organize_me.exceptions import TaskNotFoundError
from tests.test_task import dummy_dates


@pytest.fixture
def task_manager() -> TaskApi:
    """Fixture to initialize a fresh TaskApi instance."""
    return TaskApi()


@pytest.fixture
def dummy_tasks() -> Dict[int, Task]:
    """Fixture to provide a set of dummy tasks."""
    return {
        1: Task(id=1, title='Task 1'),
        2: Task(id=2, title='Task 2', description='Description 2'),
        3: Task(id=3, title='Task 3', description='Description 3', start_date='2021-01-01', end_date='2021-01-02')
    }


@pytest.fixture(scope='function', autouse=True)
def remove_json_file() -> None:
    """Fixture to remove the JSON file before and after each test."""
    if os.path.exists(TaskApi.JSON_FILE):
        os.remove(TaskApi.JSON_FILE)


def test_save_tasks(dummy_tasks: Dict[int, Task]):
    task_manager = TaskApi(tasks=dummy_tasks)
    task_manager.save_tasks()
    assert os.path.exists(TaskApi.JSON_FILE)
    with open(TaskApi.JSON_FILE, 'r') as file:
        data = json.load(file)
    expected = {str(key): task.model_dump_json() for key, task in dummy_tasks.items()}
    assert data == expected


def test_read_json(dummy_tasks):
    task_manager = TaskApi(tasks=dummy_tasks)
    task_manager.save_tasks()
    assert os.path.exists(TaskApi.JSON_FILE)
    task_manager_2 = TaskApi()
    assert task_manager_2.tasks == dummy_tasks


def test_update_task_invalid_id(task_manager):
    with pytest.raises(TaskNotFoundError):
        task_manager.update(1, title='New Task 1')


def add_task(task_manager, dummy_dates):
    title, desc, start, end = 'Task 1', 'Description 1', dummy_dates['start_date'], dummy_dates['end_date']
    data = {'title': title, 'description': desc, 'start_date': start, 'end_date': end}
    task_id = task_manager.add(**data)
    return task_id


def test_add_task(task_manager, dummy_dates):
    task_id = add_task(task_manager, dummy_dates)
    task = task_manager.get_task(task_id)
    assert task.start_date == dummy_dates['start_date']


def test_update_task(task_manager, dummy_dates):
    task_id = add_task(task_manager, dummy_dates)
    new_title = 'New Task 1'
    task_manager.update(task_id, title=new_title)
    task = task_manager.get_task(task_id)
    assert task.title == new_title
    assert task.start_date == dummy_dates['start_date']


def test_delete_task(task_manager, dummy_dates):
    task_id = add_task(task_manager, dummy_dates)
    assert task_manager.get_task(task_id) is not None
    task_manager.delete(task_id)
    with pytest.raises(TaskNotFoundError):
        task_manager.get_task(task_id)


if __name__ == '__main__':
    pytest.main()
