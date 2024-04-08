import json
import pathlib

from config import ROOT_DIR


class Vacancy:
    def __init__(self, vacancy_dict):
        self.name = vacancy_dict['name']
        if not vacancy_dict.get('salary'):
            self.__salary = None
            self.salary_from = 0
            self.salary_to = 0
        else:
            self.salary_from = vacancy_dict.get('salary').get('from')
            self.salary_to = vacancy_dict.get('salary').get('to')
        self.employer = vacancy_dict['employer']['name']
        self.currency = self.get_currency(vacancy_dict['salary'])
        self.experience = vacancy_dict['experience']['name']
        self.schedule = vacancy_dict['schedule']['name']
        self.employment = vacancy_dict['employment']['name']
        self.requirement = self.check_source_info(vacancy_dict['snippet']['requirement'])
        self.responsibility = self.check_source_info(vacancy_dict['snippet']['responsibility'])
        self.professional_roles = ', '.join(
            [professional_role['name'] for professional_role in
             vacancy_dict['professional_roles']])
        self.url = vacancy_dict['alternate_url']

    @staticmethod
    def check_source_info(value):
        if value:
            return value
        return 'информация не была найдена'

    def get_currency(self, currency):
        try:
            return self.convert_currency(currency.get('currency'))
        except KeyError:
            return 'тип валюты не указан'
        except AttributeError:
            return 'тип валюты не указан'

    def convert_currency(self, currency):
        if currency in ['RUR', 'KZT', 'BYR', 'UZS']:
            if currency == 'RUR':
                return 'руб.'
            elif currency == 'KZT':
                return 'тенге'
            elif currency == 'BYR':
                return 'белорус. руб.'
            elif currency == 'UZS':
                return 'узбек. сум'
        else:
            return (f'неизвестный тип валюты '
                    f'с кодовым обозначением {self.currency}')

    def get_salary(self):
        if not (self.salary_from or self.salary_to):
            return "Заработная плата: не указана"
        else:
            if not self.salary_from:
                return (f"Заработная плата: до "
                        f"{self.salary_to} {self.currency}")
            if not self.salary_to:
                return (f"Заработная плата: от {self.salary_from} "
                        f"{self.currency}")
            return (f"Заработная плата: от {self.salary_from} до "
                    f"{self.salary_to} {self.currency}")

    @classmethod
    def get_list_with_objects(cls, list_with_vacancies):
        returned_list = []
        for vacancy in list_with_vacancies:
            vacancy_object = cls(vacancy)
            returned_list.append(vacancy_object)
        return returned_list

    def __eq__(self, other):  # – для равенства ==
        if isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from == other.salary_from
        return self.salary_from == other

    def __ne__(self, other):  # – для неравенства !=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from != other.salary_from
        return self.salary_from != other

    def __lt__(self, other):  # – для оператора меньше <
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from < other.salary_from
        return self.salary_from < other

    def __le__(self, other):  # – для оператора меньше или равно <=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from <= other.salary_from
        return self.salary_from <= other

    def __gt__(self, other):  # – для оператора больше >
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from > other.salary_from
        return self.salary_from > other

    def __ge__(self, other):  # – для оператора больше или равно >=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")
        if type(other) is type(self):
            return self.salary_from >= other.salary_from
        return self.salary_from >= other

    def __str__(self):
        return (f'============================================================'
                f'\nВакансия: {self.name}\n'
                f'{self.get_salary()}\n'
                f'Наниматель: {self.employer}\n'
                f'Опыт работы: {self.experience}\n'
                f'График работы: {self.schedule}\n'
                f'Занятость: {self.employment}\n'
                f'Требования: {self.requirement.replace("<highlighttext>", "").replace("</highlighttext>", "")}\n'
                f'Обязанности: {self.responsibility.replace("<highlighttext>", "").replace("</highlighttext>", "")}\n'
                f'Название должности: {self.professional_roles}\n'
                f'Ссылка на страницу вакансии: {self.url}\n'
                f'============================================================')


if __name__ == '__main__':
    TEST_PATH = pathlib.Path.joinpath(ROOT_DIR, 'data', 'test_vacancies.json')
    with open(TEST_PATH, 'r', encoding='utf-8') as file:
        list_vacation = json.load(file)
    for vacation in Vacancy.get_list_with_objects(list_vacation["items"]):
        print(vacation)
