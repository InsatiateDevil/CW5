from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        pass
