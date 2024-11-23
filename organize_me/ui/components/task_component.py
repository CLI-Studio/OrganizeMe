from dataclasses import dataclass
from pickle import TUPLE
from typing import Any, ClassVar, List, Tuple
from organize_me.app.task import Task


@dataclass(frozen=True)
class Option:
    key: str
    name: str
    description: str


class TaskComponent:
    OPTIONS: ClassVar[List[Option]] = [
        Option(key="d", name="delete", description="Delete task"),
        Option(key="u", name="update", description="Update task"),
        Option(key="c", name="complete", description="Complete task"),
        Option(key="i", name="incomplete", description="Incomplete task"),
    ]

    @property
    def options(self) -> List[Option]:
        return self.OPTIONS

    @property
    def component(self) -> Tuple[Any, ...]:
        return (
            self._task.id,
            self._task.title,
            self._task.description,
            self._task.start_date,
            self._task.end_date,
        )

    @property
    def is_complete(self) -> bool:
        return bool(self._task.end_date)

    def __init__(self, task: Task):
        self._task = task

    def on_delete(self):
        print(f"Deleting task: {self._task.title}")

    def on_update(self, new_task: Task):
        print(f"Updating task: {self._task.id}")
        self._task = new_task

    def on_complete(self):
        print(f"Completing task: {self._task.title}")

    def on_incomplete(self):
        print(f"Marking task incomplete: {self._task.title}")
