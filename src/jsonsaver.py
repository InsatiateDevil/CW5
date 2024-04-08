import json
import pathlib

from config import ROOT_DIR
from src.saver import Saver


class JSONSaver(Saver):
    def __init__(self, path):
        self.path = path

    def write_vacancy(self, vacancies):
        with open(self.path, 'w', encoding='utf-8') as file:
            for vacancy in vacancies:
                json.dump(vacancy.__dict__, file, ensure_ascii=False)

    def add_vacancy(self, vacancies):
        with open(self.path, '+a', encoding='utf-8') as file:
            for vacancy in vacancies:
                print(vacancy.__dict__)
                json.dump(vacancy.__dict__, file, ensure_ascii=False)
                file.write(', ')

    def del_vacancy(self, vacancy):
        with open(self.path, 'rw', encoding='utf-8') as file:
            text = file.read()
            for vac in text:
                if str(vac) == str(vacancy):
                    del vac
            file.write(text)
