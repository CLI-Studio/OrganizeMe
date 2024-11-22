from organize_me.app.task_api import TaskApi
from organize_me.app.layout import Layout
from organize_me.app.task import Task
from organize_me.app.api import Api
from datetime import datetime
from typing import Optional, Dict


class Controller:
    def __init__(self, tasks: Optional[Dict[int, Task]] = None):
        self.api: Api = TaskApi(tasks)
        self.app_layout = Layout(api=self.api)

    def run(self) -> None:
        self.app_layout.run()


def test_controller() -> Controller:
    tasks = {
        1: Task(id=1, title='Task 1', description='Description 1 ', start_date=datetime.now(), end_date=datetime.now()),
        2: Task(id=2, title='Task 2'),
    }
    return Controller(tasks)


if __name__ == '__main__':
    controller = test_controller()
    # controller = Controller()
    controller.run()
