from typing import Any, Dict, List
from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Label
from textual.coordinate import Coordinate
from textual.widgets.data_table import RowKey
from textual.containers import Vertical

from organize_me.app.api import Api
from organize_me.app.exceptions import EmptyObjectDataError
from organize_me.app.layout_validation import (validate_table_exists, validate_table_not_empty,
                                               validate_item_exists, safe_action)
# Example API for testing
from organize_me.app.exampleApi import ExampleApi


def format_long_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


class Layout(App[Any]):
    OBJ_ID_COL = 0
    CSS_PATH = "css/layout.tcss"
    BINDINGS = [
        ("a", "add", "add a new row"),
        ("u", "update", "update the current row"),
        ("r", "remove", "remove the current row"),
        ("q", "quit", "Quit the application"),
    ]

    def __init__(self, api: Api) -> None:
        super().__init__()
        if not api.fields():
            raise EmptyObjectDataError()
        self.api = api
        self.table: DataTable[Any] = DataTable(cursor_type="row")
        self.label_status = Label("", name="status")

    def on_mount(self) -> None:
        # TODO: can moved to css file, change the datatable division to main-container and overall-footer ids
        self.query_one(DataTable).styles.height = "99%"
        self.query_one(Label).styles.height = "auto"
        self.query_one(Footer).styles.height = "auto"

    def compose(self) -> ComposeResult:
        """Compose the UI components."""
        columns, data = self.api.data()
        data = self._convert_dates_to_str(data)
        self.table.add_columns(*columns)
        self.table.add_rows(data)
        yield Vertical(
            self.table,
            self.label_status,
            Footer(),
            id="main_container",
        )

    def update_label_status(self, text: str) -> None:
        """Update the status label with the provided text."""
        self.label_status.update(text)

    @safe_action
    @validate_table_exists
    @validate_table_not_empty
    def action_remove(self) -> None:
        """Remove the selected row from the table."""
        self.api.delete(self.get_object_id())
        self.table.remove_row(self.get_row_key())
        self.update_label_status("row removed")

    @safe_action
    @validate_table_exists
    def action_add(self) -> None:
        """Add a new item to the table."""
        # TODO: Implement the modal screen that will display a form to add a new item
        # TODO: The screen will return a dictionary of the form values (like the raw_data below)
        raw_data = {"id": 2, "name": "name", "age": 25, "date": "2021-01-01"}
        self.add_item_callback(raw_data)
        # self.push_screen(screen=AddItemScreen(), callback=self.add_item_callback, modal=True)
        self.update_label_status("row added")

    @validate_item_exists
    def add_item_callback(self, item: Dict[str, object]) -> None:
        """Callback for adding a new item to the API and table."""
        self.api.add(**item)
        self.table.add_row(*item.values())

    @safe_action
    @validate_table_exists
    @validate_table_not_empty
    def action_update(self) -> None:
        """Update the currently selected row with new data."""
        raw_data = dict(zip(self.get_column_labels(), self.table.get_row(self.get_row_key())))
        # Simulating an update to the name for demonstration
        raw_data["name"] = "updated name"
        self.update_item_callback(raw_data)
        # self.push_screen(screen=AddItemScreen(raw_data), callback=self.add_item_callback, modal=True)

    @validate_item_exists
    def update_item_callback(self, item: Dict[str, str]) -> None:
        """Callback for updating an existing item in the API and table."""
        self.api.update(self.get_object_id(), **item)
        for col_index, col_name in enumerate(self.get_column_labels()):
            coord_to_update = Coordinate(self.table.cursor_coordinate.row, col_index)
            if col_name in item:
                self.table.update_cell_at(coord_to_update, item[col_name], update_width=True)

    def get_column_labels(self) -> List[str]:
        """Retrieve the labels of the columns in the table."""
        return [col.label.plain for col in self.table.columns.values()]

    def get_object_id(self) -> int:
        """Get the object ID of the currently selected row."""
        coords = self.table.cursor_coordinate
        id_coords = Coordinate(coords.row, self.OBJ_ID_COL)
        return int(self.table.get_cell_at(id_coords))

    def get_row_key(self) -> RowKey:
        """Get the row key of the currently selected row."""
        coords = self.table.cursor_coordinate
        return self.table.coordinate_to_cell_key(coords)[0]

    @staticmethod
    def _convert_dates_to_str(data: List[List[Any]]) -> List[List[str | None]]:
        """Convert datetime objects in data to string representation."""
        return [
            [format_long_date(value) if isinstance(value, datetime) else value for value in row]
            for row in data
        ]


def example_app() -> Layout:
    """Create an instance of the application with an example API."""
    api: Api = ExampleApi()
    return Layout(api=api)


if __name__ == "__main__":
    app = example_app()
    app.run()
