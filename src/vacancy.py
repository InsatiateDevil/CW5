import json
import pathlib

from config import ROOT_DIR


class Vacancy:
    def __init__(self, name, salary_from, salary_to, employer, currency,
                 experience, schedule, employment, requirement, responsibility,
                 professional_roles, url):
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.employer = employer
        self.currency = currency
        self.experience = experience
        self.schedule = schedule
        self.employment = employment
        self.requirement = requirement
        self.responsibility = responsibility
        self.professional_roles = professional_roles
        self.url = url

    @classmethod
    def get_list_with_objects(cls, list_with_vacancies):
        returned_list = []
        for vacancy in list_with_vacancies:
            name = vacancy['name']
            if not vacancy.get('salary'):
                salary_from = 0
                salary_to = 0
                currency = 0
            else:
                salary_from = vacancy.get('salary').get('from')
                salary_to = vacancy.get('salary').get('to')
                currency = cls.check_source_info(vacancy['salary']['currency'])
            employer = vacancy['employer']['name']
            experience = vacancy['experience']['name']
            schedule = vacancy['schedule']['name']
            employment = vacancy['employment']['name']
            requirement = cls.check_source_info(
                vacancy['snippet']['requirement'])
            responsibility = cls.check_source_info(
                vacancy['snippet']['responsibility'])
            professional_roles = ', '.join(
                [professional_role['name'] for professional_role in
                 vacancy['professional_roles']])
            url = vacancy['alternate_url']
            vacancy_object = cls(name, salary_from, salary_to, employer,
                                 currency, experience, schedule, employment,
                                 requirement, responsibility,
                                 professional_roles, url)
            returned_list.append(vacancy_object)
        return returned_list

    @classmethod
    def get_objects_list_from_objects_dict(cls, list_with_vacancies):
        returned_list = []
        for vacancy in list_with_vacancies:
            name = vacancy['name']
            salary_from = vacancy['salary_from']
            salary_to = vacancy['salary_to']
            currency = vacancy['currency']
            employer = vacancy['employer']
            experience = vacancy['experience']
            schedule = vacancy['schedule']
            employment = vacancy['employment']
            requirement = vacancy['requirement']
            responsibility = vacancy['responsibility']
            professional_roles = vacancy['professional_roles']
            url = vacancy['url']
            vacancy_object = cls(name, salary_from, salary_to, employer,
                                 currency, experience, schedule, employment,
                                 requirement, responsibility,
                                 professional_roles, url)
            returned_list.append(vacancy_object)
        return returned_list

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
        if currency:
            if currency == 'RUR':
                return 'руб.'
            elif currency == 'KZT':
                return 'тенге'
            elif currency == 'BYR':
                return 'белорус. руб.'
            elif currency == 'UZS':
                return 'узбек. сум'
            elif currency == 'EUR':
                return 'евро'
            elif currency == 'USD':
                return 'долларов'
        elif currency == 0:
            return 'валюта не была указана'
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
            if self.salary_from == self.salary_to:
                return (f"Заработная плата: {self.salary_from} "
                        f"{self.currency}")
            return (f"Заработная плата: от {self.salary_from} до "
                    f"{self.salary_to} {self.currency}")

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
