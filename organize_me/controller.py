from organize_me.task_api import TaskApi
from organize_me.layout import Layout
from organize_me.task import Task
from organize_me.api import Api
from datetime import datetime


class Controller:
    def __init__(self, tasks=None) -> None:
        self.api: Api = TaskApi(tasks)
        columns, data = self.api.data()
        self.app_layout = Layout(columns, data)

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
