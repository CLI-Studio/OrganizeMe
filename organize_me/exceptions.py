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


class DateStrFormatError(Exception):
    """Raised when a task date is invalid."""
    def __init__(self, date: str) -> None:
        self.message = f"Invalid date format: {date}, must be in ISO format"
        super().__init__(self.message)


class DateTypeError(Exception):
    """Raised when a task date is invalid."""
    def __init__(self, date: str) -> None:
        self.message = f"Invalid date type: {date}, must be a string or a datetime object"
        super().__init__(self.message)


class EmptyObjectDataError(Exception):
    """Raised when an object is empty."""
    def __init__(self) -> None:
        self.message = "Object data is empty"
        super().__init__(self.message)
