from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Label
from typing import Any, Optional
from datetime import datetime
from organize_me.api import Api
from organize_me.exceptions import EmptyObjectDataError
from textual.coordinate import Coordinate
# example api for testing
from organize_me.exampleApi import ExampleApi


def long_dates(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


# using App[Any] to silence mypy
class Layout(App[Any]):
    OBJ_ID_COL = 0
    CSS_PATH = "css/layout.tcss"
    BINDINGS = [
        ("r", "remove", "remove the current row"),
        ("q", "quit", "Quit the application"),
    ]

    def __init__(self, api: Api) -> None:
        super().__init__()
        self.api = api
        self.table: DataTable[Any] = DataTable()
        self.table.cursor_type = "row"

    def on_mount(self) -> None:
        pass

    @staticmethod
    def _convert_dates_to_str(data: list[list[Any]]) -> list[list[str | Any]]:
        return [
            [long_dates(value) if isinstance(value, datetime) else value for value in row]
            for row in data
        ]

    def compose(self) -> ComposeResult:
        columns, data = self.api.data()
        data = self._convert_dates_to_str(data)
        if not columns:
            raise EmptyObjectDataError()
        self.table.add_columns(*columns)
        self.table.add_rows(data)
        yield self.table
        yield Footer()

    def action_remove(self) -> None:
        table = self.table
        coords = table.cursor_coordinate
        id_coords = Coordinate(coords.row, self.OBJ_ID_COL)
        id_object = int(table.get_cell_at(id_coords))
        self.api.delete(id_object)
        row_key, _ = table.coordinate_to_cell_key(coords)
        table.remove_row(row_key)


def example_app() -> Layout:
    api: Api = ExampleApi()
    return Layout(api=api)


if __name__ == "__main__":
    app = example_app()
    app.run()
