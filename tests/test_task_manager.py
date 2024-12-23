import os
import json
import pytest
from organize_me.task_manager import TaskManager
from organize_me.task import Task
from organize_me.exceptions import TaskNotFoundError
from tests.test_task import dummy_dates


@pytest.fixture
def task_manager():
    return TaskManager()


@pytest.fixture
def dummy_tasks():
    return {
        1: Task(id=1, title='Task 1'),
        2: Task(id=2, title='Task 2', description='Description 2'),
        3: Task(id=3, title='Task 3', description='Description 3', start_date='2021-01-01', end_date='2021-01-02')
    }


@pytest.fixture(scope='function', autouse=True)
def remove_json_file():
    if os.path.exists(TaskManager.JSON_FILE):
        os.remove(TaskManager.JSON_FILE)


def test_save_tasks(dummy_tasks):
    task_manager = TaskManager(tasks=dummy_tasks)
    task_manager.save_tasks()
    assert os.path.exists(TaskManager.JSON_FILE)
    with open(TaskManager.JSON_FILE, 'r') as file:
        data = json.load(file)
    expected = {str(key): task.model_dump_json() for key, task in dummy_tasks.items()}
    assert data == expected


def test_read_json(dummy_tasks):
    task_manager = TaskManager(tasks=dummy_tasks)
    task_manager.save_tasks()
    assert os.path.exists(TaskManager.JSON_FILE)
    task_manager_2 = TaskManager()
    assert task_manager_2.tasks == dummy_tasks


def test_add_task(task_manager, dummy_dates):
    title, desc, start, end = 'Task 1', 'Description 1', dummy_dates['start_date'], dummy_dates['end_date']
    task_id = task_manager.add_task(title=title, description=desc, start_date=start, end_date=end)
    task = task_manager.get_task(task_id)
    assert task.title == title
    assert task.description == desc


def test_update_task(task_manager, dummy_dates):
    title, desc, start, end = 'Task 1', 'Description 1', dummy_dates['start_date'], dummy_dates['end_date']
    task_id = task_manager.add_task(title=title, description=desc, start_date=start, end_date=end)
    new_title = 'New Task 1'
    task_manager.update_task(task_id=task_id, title=new_title)
    task = task_manager.get_task(task_id)
    assert task.title == new_title
    assert task.description == desc


def test_update_task_invalid_id(task_manager):
    with pytest.raises(TaskNotFoundError):
        task_manager.update_task(task_id=-1, title='Invalid Task')


if __name__ == '__main__':
    pytest.main()
