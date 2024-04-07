import json
import pathlib

from config import ROOT_DIR
from src.saver import Saver


class JSONSaver(Saver):
    def __init__(self):
        self.file = pathlib.Path.joinpath(ROOT_DIR, 'vacancies.json')

    def write_vacancy(self, vacancy):
        with open(self.file, '+a', encoding='utf-8') as file:
            json.dump(vacancy, file, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        with open(self.file, '+a', encoding='utf-8') as file:
            json.dump(vacancy, file, ensure_ascii=False)

    def del_vacancy(self, vacancy):
        with open(self.file, 'rw', encoding='utf-8') as file:
            text = file.read()
            for vac in text:
                if str(vac) == str(vacancy):
                    del vac
            file.write(text)
