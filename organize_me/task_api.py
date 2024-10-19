import os
import json
import uuid
from abc import ABC
from datetime import datetime
from typing import Optional, Dict
from organize_me.exceptions import DuplicateIdError, TaskNotFoundError
from organize_me.task import Task
from organize_me.api import Api


class TaskApi(Api):
    JSON_FILE = os.path.join(os.getcwd(), 'tasks.json')

    def __init__(self, tasks: Optional[Dict[int, Task]] = None):
        self.tasks: Dict[int, Task] = tasks or self.read_json()

    def save_tasks(self) -> None:
        with open(self.JSON_FILE, 'w') as outfile:
            json.dump(self._tasks_to_json(), outfile)

    def _tasks_to_json(self) -> Dict[int, str]:
        return {task_id: task.model_dump_json() for task_id, task in self.tasks.items()}

    @staticmethod
    def _json_to_tasks(data: Dict[int, str]) -> Dict[int, Task]:
        return {int(task_id): Task.model_validate_json(task_json) for task_id, task_json in data.items()}

    def read_json(self) -> Dict[int, Task]:
        if os.path.exists(self.JSON_FILE):
            with open(self.JSON_FILE, 'r') as file:
                return self._json_to_tasks(json.load(file))
        return {}

    def add_task(self, title: str, description: Optional[str] = None,
                 start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> int:
        task_id = self._generate_task_id()
        self.tasks[task_id] = Task(
            id=task_id, title=title, description=description,
            start_date=start_date, end_date=end_date
        )
        return task_id

    def _generate_task_id(self) -> int:
        while True:
            task_id = uuid.uuid4().int
            if task_id not in self.tasks:
                return task_id
            raise DuplicateIdError(task_id)

    def get_task(self, task_id: int) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> None:
        task = self.get_task(task_id)
        task.update(
            title=title, description=description,
            start_date=start_date, end_date=end_date
        )
        self.save_tasks()

    def data(self) -> tuple:
        return Task.model_fields.keys(), [task.__dict__.values() for task in self.tasks.values()]
