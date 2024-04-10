import pathlib
import requests
import json

from config import ROOT_DIR

url_post = "https://api.hh.ru/vacancies"
TEST_VACATIONS = pathlib.Path.joinpath(ROOT_DIR, 'test_vacancies.json')


def user_interact():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации "
                         "вакансий через пробел: ").split(" ")
    min_salary = int(input("Введите нижний порог заработной платы: "))
    return search_query, top_n, filter_words, min_salary


def get_filtered_vacancies(vacancies_list, words_for_filter):
    filtered_list = []
    for vacancy in vacancies_list:
        for word in words_for_filter:
            if word in vacancy.responsibility or word in vacancy.requirement:
                filtered_list.append(vacancy)
                break
    return filtered_list


def get_vacancies_by_salary(vacancies, min_salary):
    only_salary_vacancies = []
    for vacancy in vacancies:
        if vacancy >= min_salary:
            only_salary_vacancies.append(vacancy)
    return only_salary_vacancies


def get_sorted_vacancies(vacancies):
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies, stop):
    return vacancies[:stop]


def print_vacancies(vacancies):
    for vacancy in vacancies:
        print(vacancy)
