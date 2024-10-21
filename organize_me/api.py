from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Api(ABC):
    @abstractmethod
    def data(self) -> tuple[List[str], List[Any]]:
        """
        Extract data from the API

        Returns:
            tuple: columns(list of strings) and the database data(list of tuples)
        """
        pass

    @abstractmethod
    def add(self, **kwargs: Dict[str, Any]) -> int:
        """
        Add data to the API

        Args:
            **kwargs: data to be added

        Returns:
            int: the id of the added data

        """
        pass

    @abstractmethod
    def update(self, o_id: int, **kwargs: Dict[str, Any]) -> None:
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
