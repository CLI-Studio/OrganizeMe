from task_manager import TaskManager
from layout import Layout
from task import Task


class Controller:
    def __init__(self, tasks=None):
        self.tm = TaskManager(tasks)
        columns, data = self.tm.extract_data()
        print(type(columns), columns)
        print(type(data[0]), data[0])
        self.app_layout = Layout(columns, data)

    def run(self):
        self.app_layout.run()


def test_controller() -> Controller:
    tasks = {
        1: Task(id=1, title='Task 1', description='Description 1 dfu cjgfk', start_date='2022-01-01', end_date='2026-01-02'),
        2: Task(id=2, title='Task 2', start_date='2021-01-01', end_date='2021-01-02')
    }
    return Controller(tasks)


if __name__ == '__main__':
    controller = test_controller()
    # controller = Controller()
    controller.run()
