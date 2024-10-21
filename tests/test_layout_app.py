import pytest
from organize_me.layout import Layout as App


@pytest.fixture
def users_data_app():
    columns = ["id", "name", "age"]
    data = [
        (1, "Alice", 24),
        (2, "Bob", 25),
        (3, "Charlie", 26),
    ]
    return {
        "app": App(columns, data),
        "columns": columns,
        "data": data,
    }


@pytest.fixture
def empty_app():
    return {
        "app": App([], []),
        "columns": [],
        "data": [],
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("app_fixture", ["users_data_app", "empty_app"])
async def test_layout_app(request, app_fixture):
    app, columns, data = request.getfixturevalue(app_fixture).values()
    async with app.run_test():
        table = app.data_table
        assert table is not None
        assert columns == [str(value.label) for value in table.columns.values()]


@pytest.mark.asyncio
@pytest.mark.parametrize("app_fixture", ["users_data_app", "empty_app"])
async def test_cursor_down(request, app_fixture):
    app, columns, data = request.getfixturevalue(app_fixture).values()
    async with app.run_test():
        table = app.data_table
        assert table is not None
        assert table.cursor_row == 0
        if data:
            table.action_cursor_down()
            assert table.cursor_row == 1
        for i in range(len(data)):
            table.action_cursor_down()
        # Cursor should not go beyond the last row
        assert table.cursor_row == max(0, len(data) - 1)


if __name__ == "__main__":
    pytest.main()
