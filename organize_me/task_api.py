import os
import json
import uuid
from typing import Optional, Dict, Any, List, Callable
from organize_me.exceptions import TaskNotFoundError
from organize_me.task import Task
from organize_me.api import Api


class TaskApi(Api):
    JSON_FILE = os.path.join(os.getcwd(), 'tasks.json')

    def __init__(self, tasks: Optional[Dict[int, Task]] = None):
        self.tasks: Dict[int, Task] = tasks or self.read_json()

    def fields(self) -> dict[str, Callable[[str], Any]]:
        return Task.fields()

    def data(self) -> tuple[List[str], List[List[Any]]]:
        return list(Task.model_fields.keys()), [list(task.__dict__.values()) for task in self.tasks.values()]

    def add(self, **kwargs: Any) -> int:
        task_id: int = self._generate_task_id() if 'id' not in kwargs else kwargs['id']
        data = self.serialize_data(**kwargs)
        self.tasks[task_id] = Task(id=task_id, **data)
        return task_id

    def update(self, o_id: int, **kwargs: Any) -> None:
        self.get_task(o_id).update(**kwargs)
        self.save_tasks()

    def delete(self, o_id: int) -> None:
        if o_id not in self.tasks:
            raise TaskNotFoundError(o_id)
        self.tasks.pop(o_id)
        self.save_tasks()

    def save_tasks(self) -> None:
        with open(self.JSON_FILE, 'w') as outfile:
            json.dump(self._tasks_to_json(self.tasks), outfile)

    @staticmethod
    def _tasks_to_json(data: Dict[int, Task]) -> Dict[int, str]:
        return {task_id: task.model_dump_json() for task_id, task in data.items()}

    @staticmethod
    def _json_to_tasks(data: Dict[int, str]) -> Dict[int, Task]:
        return {int(task_id): Task.model_validate_json(task_json) for task_id, task_json in data.items()}

    def read_json(self) -> Dict[int, Task]:
        if os.path.exists(self.JSON_FILE):
            with open(self.JSON_FILE, 'r') as file:
                return self._json_to_tasks(json.load(file))
        return {}

    def _generate_task_id(self) -> int:
        while True:
            task_id = uuid.uuid4().int
            if task_id not in self.tasks:
                return task_id

    def get_task(self, task_id: int) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task
