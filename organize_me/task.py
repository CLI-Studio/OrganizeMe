from datetime import datetime
from typing import Optional, ClassVar, Any, Dict, Callable
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict


class Task(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    ERROR_ID_MUST_BE_POSITIVE: ClassVar[str] = "Task ID must be a positive integer."
    ERROR_TITLE_EMPTY: ClassVar[str] = "Title cannot be empty or only whitespace."
    ERROR_DATE_RANGE_MISSING: ClassVar[str] = "Both start and end dates must be provided."
    ERROR_END_DATE_BEFORE_START: ClassVar[str] = "End date cannot be before the start date."
    ERROR_CREATE_DATE_IN_FUTURE: ClassVar[str] = "Creation date cannot be set in the future."

    id: int = Field(frozen=True)
    title: str = Field(...)
    description: Optional[str] = Field(default=None)
    create_date: datetime = Field(default_factory=datetime.now, frozen=True)
    update_date: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)

    @staticmethod
    def fields() -> Dict[str, Callable[[str], Any]]:

        def date_convert(date_input: str or None or datetime) -> Optional[datetime]:
            if date_input and isinstance(date_input, str):
                return datetime.fromisoformat(date_input)
            return date_input

        return {
            "id": int,
            "title": str,
            "description": str,
            "create_date": lambda x: date_convert(x),
            "update_date": lambda x: date_convert(x),
            "start_date": lambda x: date_convert(x),
            "end_date": lambda x: date_convert(x),
        }

    # noinspection PyNestedDecorators
    @field_validator('id')
    @classmethod
    def validate_id(cls, value: int) -> int:
        if value <= 0:
            raise ValueError(cls.ERROR_ID_MUST_BE_POSITIVE)
        return value

    # noinspection PyNestedDecorators
    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(cls.ERROR_TITLE_EMPTY)
        return value.strip()

    # noinspection PyNestedDecorators
    @field_validator('description')
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if value else value

    # noinspection PyNestedDecorators
    @field_validator('create_date')
    @classmethod
    def validate_create_date(cls, value: datetime) -> datetime:
        if value > datetime.now():
            raise ValueError(cls.ERROR_CREATE_DATE_IN_FUTURE)
        return value

    # noinspection PyNestedDecorators
    @model_validator(mode='before')
    @classmethod
    def validate_date_range(cls, values: dict[str, Optional[datetime]]) -> dict[str, Optional[datetime]]:
        start_date = values.get('start_date')
        end_date = values.get('end_date')
        if (start_date and not end_date) or (end_date and not start_date):
            raise ValueError(cls.ERROR_DATE_RANGE_MISSING)
        if start_date and end_date and end_date < start_date:
            raise ValueError(cls.ERROR_END_DATE_BEFORE_START)
        return values

    def __setattr__(self, key: str, value: Any) -> None:
        super().__setattr__(key, value)
        if key != 'update_date':
            self.update_date = datetime.now()

    def update(self, **kwargs: Any) -> None:
        for field, value in kwargs.items():
            if value is not None and field in self.model_fields:
                setattr(self, field, value)
        self.__validate__()

    def __validate__(self) -> None:
        self.__class__.model_validate(self.model_dump())
