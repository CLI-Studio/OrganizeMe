from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable


class Api(ABC):
    @abstractmethod
    def data(self) -> tuple[List[str], List[List[Any]]]:
        """
        Extract data from the API

        Returns:
            tuple: columns(list of strings) and the database data(list of tuples)
        """
        pass

    @abstractmethod
    def add(self, **kwargs: Any) -> int:
        """
        Add data to the API

        Args:
            **kwargs: data to be added

        Returns:
            int: the id of the added data

        """
        pass

    @abstractmethod
    def update(self, o_id: int, **kwargs: Any) -> None:
        """
        Update data in the API

        Args:
            :param o_id: the id of the data to be updated
            **kwargs: data to be updated

        """
        pass

    @abstractmethod
    def delete(self, o_id: int) -> None:
        """
        Delete data from the API

        Args:
            :param o_id: the id of the data to be deleted

        """
        pass

    @abstractmethod
    def fields(self) -> Dict[str, Callable[[str], Any]]:
        """
        Get the fields of the data

        Returns:
            dict: the fields of the data, where the key is the field name and the value
                is the field type / function to convert from a string to the relevant type
        """
        pass

    # layout pass to api dict of keys and values, that is the input of the user
    # the api will convert the data to the relevant type and add it to the database
    def serialize_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Serialize the data

        Args:
            **kwargs: the data to be serialized

        Returns:
            dict: the serialized data
        """
        fields = self.fields()
        for key, value in kwargs.items():
            if key in fields:
                try:
                    kwargs[key] = fields[key](value)  # fields[key] is conversion function
                except Exception:
                    raise TypeError(f"serialization failed, could not convert {value} to {fields[key]}")
            else:
                raise KeyError(f"serialization failed due to key {key} not in fields")
        return kwargs
