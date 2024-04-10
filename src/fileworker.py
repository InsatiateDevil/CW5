from abc import ABC, abstractmethod


class FileWorker(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self):
        pass

    @abstractmethod
    def add_vacancies(self, vacancies):
        pass

    @abstractmethod
    def write_vacancies(self, vacancies):
        pass

    @abstractmethod
    def del_vacancies(self, vacancies):
        pass
