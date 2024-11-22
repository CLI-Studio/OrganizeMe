# tests/test_task.py
import pytest
from datetime import datetime, timedelta
from organize_me.app.task import Task


@pytest.fixture
def dummy_dates():
    """Provides start and end dates for testing."""
    return {
        "start_date": datetime.now() - timedelta(days=1),
        "end_date": datetime.now() + timedelta(days=10)
    }


class TestTask:
    def test_valid_task_creation(self, dummy_dates):
        task = Task(
            id=1,
            title="Test Task",
            description="A test task description",
            start_date=dummy_dates['start_date'],
            end_date=dummy_dates['end_date']
        )
        assert task.title == "Test Task"
        assert task.start_date == dummy_dates['start_date']
        assert task.end_date == dummy_dates['end_date']
        assert task.description == "A test task description"
        assert task.create_date is not None
        assert task.update_date is not None

    def test_valid_task_with_create_date(self, dummy_dates):
        create_date = datetime.now()
        task = Task(
            id=1,
            title="Test Task",
            description="A test task description",
            start_date=dummy_dates['start_date'],
            end_date=dummy_dates['end_date'],
            create_date=create_date
        )
        assert task.create_date == create_date

    def test_minimal_valid_task(self):
        task = Task(id=1, title="Test Task")
        assert task.title == "Test Task"
        assert task.create_date is not None
        assert task.update_date is not None
        assert task.start_date is None
        assert task.end_date is None
        assert task.description is None

    @pytest.mark.parametrize("invalid_id", [0, -1])
    def test_id_validation(self, invalid_id):
        with pytest.raises(ValueError, match=Task.ERROR_ID_MUST_BE_POSITIVE):
            Task(id=invalid_id, title="Test Task")

    @pytest.mark.parametrize("invalid_title", ["", " ", "  "])
    def test_title_validation(self, invalid_title):
        with pytest.raises(ValueError, match=Task.ERROR_TITLE_EMPTY):
            Task(id=1, title=invalid_title)

    def test_description_stripping(self):
        task = Task(id=1, title="Test Task", description="  A test task description  ")
        assert task.description == "A test task description"

    # test date validations
    def test_create_date_cannot_be_in_future(self, dummy_dates):
        future_date = datetime.now() + timedelta(days=100)
        with pytest.raises(ValueError, match=Task.ERROR_CREATE_DATE_IN_FUTURE):
            Task(
                id=1,
                title="Test Title",
                start_date=dummy_dates['start_date'],
                end_date=dummy_dates['end_date'],
                create_date=future_date
            )

    def test_end_date_not_before_start_date(self, dummy_dates):
        with pytest.raises(ValueError, match=Task.ERROR_END_DATE_BEFORE_START):
            Task(
                id=1,
                title="Test Title",
                start_date=dummy_dates['end_date'],
                end_date=dummy_dates['start_date'],
            )

    def test_both_dates_required(self):
        with pytest.raises(ValueError, match=Task.ERROR_DATE_RANGE_MISSING):
            Task(id=1, title="Test Title", end_date=datetime.now())

    def test_task_with_same_dates(self):
        now = datetime.now()
        task = Task(id=1, title="Test Title", start_date=now, end_date=now)
        assert task.start_date == now
        assert task.end_date == now

    # test update methods
    def test_update_date_on_change(self, dummy_dates):
        task1 = Task(id=1, title="Test Task 1", start_date=dummy_dates['start_date'], end_date=dummy_dates['end_date'])
        task2 = Task(id=2, title="Test Task 2", start_date=dummy_dates['start_date'], end_date=dummy_dates['end_date'])
        task1.title = "Updated Test Task 1"
        assert task1.update_date > task2.update_date

    def test_update_task(self, dummy_dates):
        task = Task(id=1, title="Test Task", start_date=dummy_dates['start_date'], end_date=dummy_dates['end_date'])
        prev_update_stamp = task.update_date
        update_title, update_description = "Updated Test Task", "Updated description"
        task.update(title=update_title, description=update_description, start_date=dummy_dates['end_date'])
        assert task.title == update_title
        assert task.description == update_description
        assert task.start_date == dummy_dates['end_date']
        assert task.update_date > prev_update_stamp

    def test_update_task_invalid_title(self):
        task = Task(id=1, title="Test Task")
        with pytest.raises(ValueError, match=Task.ERROR_TITLE_EMPTY):
            task.update(title="")
        assert task.title == "Test Task"

    def test_update_task_invalid_range_dates(self, dummy_dates):
        task = Task(id=1, title="Test Task", start_date=dummy_dates['start_date'], end_date=dummy_dates['start_date'])
        with pytest.raises(ValueError, match=Task.ERROR_END_DATE_BEFORE_START):
            task.update(start_date=dummy_dates['end_date'])
        assert task.start_date == dummy_dates['start_date'] and task.end_date == dummy_dates['start_date']
