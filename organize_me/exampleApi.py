from typing import Any, Dict, List
from organize_me.api import Api


class ExampleApi(Api):
    def __init__(self) -> None:
        self.people = {
            1: [1, "Alice", "24"],
            2: [2, "Bob", "25"],
            3: [3, "Charlie", "26"],
        }

    def data(self) -> tuple[List[str], List[List[Any]]]:
        columns = ["ID", "Name", "Age"]
        return columns, list(self.people.values())

    def update(self, o_id: int, **kwargs: Dict[str, Any]) -> None:
        pass

    def add(self, **kwargs: Dict[str, Any]) -> int:
        pass

    def delete(self, o_id: int) -> None:
        if o_id in self.people:
            self.people.pop(o_id)
        else:
            raise ValueError(f"ID {o_id} not found")


if __name__ == "__main__":
    api = ExampleApi()
    print(api.data())
    api.delete(1)
    print(api.data())
    api.delete(2)
    print(api.data())
    api.delete(3)
    print(api.data())
    try:
        api.delete(4)
    except ValueError as e:
        print(e)
        print("Test passed")
