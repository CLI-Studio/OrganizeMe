from textual.app import App, ComposeResult
from textual.widgets import DataTable
from typing import Any, List, Optional
from datetime import datetime


def long_dates(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


# using App[Any] to silence mypy
class Layout(App[Any]):
    CSS_PATH = "css/layout.tcss"

    def __init__(self, columns: List[str], data: List[Any]) -> None:
        super().__init__()
        self.data_table: Optional[DataTable[Any]] = None
        self.columns = columns
        self.data = [[long_dates(value) if isinstance(value, datetime) else value for value in row] for row in data]

    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        table: DataTable[Any] = DataTable()
        table.cursor_type = "row"
        if self.columns:
            table.add_columns(*self.columns)
        if self.data:
            table.add_rows(self.data)
        self.data_table = table
        yield table


def example_app() -> Layout:
    columns = ["id", "name", "age"]
    data = [
        (1, "Alice", 24),
        (2, "Bob", 25),
        (3, "Charlie", 26),
    ]
    return Layout(columns, data)


if __name__ == "__main__":
    app = example_app()
    # app = Layout([], [])
    app.run()
