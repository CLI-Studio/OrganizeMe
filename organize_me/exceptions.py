class DuplicateIdError(Exception):
    def __init__(self, task_id: int) -> None:
        self.message = f"Task ID {task_id} already exists"
        super().__init__(self.message)


class TaskNotFoundError(Exception):
    """Raised when a task is not found."""
    def __init__(self, task_id: int) -> None:
        self.message = f"Task ID {task_id} not found in database"
        super().__init__(self.message)


class TaskIdRequiredError(Exception):
    """Raised when a task ID is required but not provided."""
    def __init__(self) -> None:
        self.message = "Task ID is required to complete this operation"
        super().__init__(self.message)
