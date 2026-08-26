from abc import ABC, abstractmethod


class Browser(ABC):

    @abstractmethod
    def create_driver(self):
        pass