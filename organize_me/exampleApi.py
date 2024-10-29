from typing import Any, List, Callable, Tuple
from organize_me.api import Api
from datetime import datetime
from random import randint

from organize_me.exceptions import DuplicateIdError


class ExampleApi(Api):
    def __init__(self) -> None:
        self.people = {
            1: {
                "id": 1,
                "name": "John",
                "age": 25,
                "date": datetime.fromisoformat("2021-01-01"),
            },
        }

    def data(self) -> Tuple[List[str], List[List[Any]]]:
        columns = ["id", "name", "age", "date"]
        return columns, [list(person.values()) for person in self.people.values()]

    def update(self, o_id: int, **kwargs: Any) -> None:
        if o_id in self.people:
            # update only the fields that are in the kwargs
            self.people[o_id] = {**self.people[o_id], **self.serialize_data(**kwargs)}
        else:
            raise ValueError(f"ID {o_id} not found")

    def add(self, **kwargs: Any) -> int:
        if "id" in kwargs and kwargs["id"] in self.people:
            raise DuplicateIdError(kwargs['id'])
        o_id: int = self.id() if "id" not in kwargs else kwargs["id"]
        self.people[o_id] = self.serialize_data(**kwargs)
        return o_id

    def id(self) -> int:
        while True:
            random = randint(1, 100)
            if random not in self.people:
                return random

    def delete(self, o_id: int) -> None:
        if o_id in self.people:
            self.people.pop(o_id)
        else:
            raise ValueError(f"ID {o_id} not found")

    def fields(self) -> dict[str, Callable[[str], Any]]:
        return {
            "id": int,
            "name": str,
            "age": int,
            "date": lambda x: datetime.fromisoformat(x),
        }

    def __str__(self) -> str:
        return str(self.people)


if __name__ == "__main__":
    api = ExampleApi()
    print(api)
    api.delete(1)
    print(api)
    api.add(id=1, name="kylie", age=25, date="2023-09-01")
    raw_data = {"id": 2, "name": "name", "age": 25, "date": "2021-01-01"}
    api.add(**raw_data)
    print(api)
    row_update = {"name": "updated", "date": "2024-07-07"}
    api.update(2, **row_update)
    print(api)
