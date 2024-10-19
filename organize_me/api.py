from abc import ABC, abstractmethod


class Api(ABC):
    @abstractmethod
    def data(self) -> tuple:
        """
        Extract data from the API

        Returns:
            tuple: columns(list of strings) and the database data(list of tuples)
        """
        pass
