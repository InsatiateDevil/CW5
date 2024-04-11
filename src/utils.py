import os
import pathlib
from config import ROOT_DIR
from src.headhunterapi import HeadHunterAPI
from src.jsonworker import JSONWorker
from src.vacancy import Vacancy

TEST_VACATIONS = pathlib.Path.joinpath(ROOT_DIR, 'test_vacancies.json')


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


def work_with_file():
    user_input = 0
    while user_input != 'назад':
        if user_input in ['стоп', 'stop']:
            break
        print('В этом блоке вы можете выгружать вакансии из файла и в '
              'последующем выполнять манипуляции с полученной информацие\n'
              'Кнопки управления:\n'
              '1 - выгрузить вакансии из файла\n'
              '2 - отфильтровать вакансии по ключевым словам\n'
              '3 - оставить вакансии с З/П, выше N\n'
              '4 - сортировать вакансии по убыванию минимальной З/П\n'
              '5 - оставить N вакансий от начала списка\n'
              '6 - распечатать информацию о всех вакансиях в текущем списке\n'
              '7 - сохранить текущий список вакансий в тот же файл\n'
              '8 - сохранить текущий список вакансий в другой файл\n')
        while user_input != 'назад':
            user_input = input(
                "Что желаете сделать? Для возврата введите 'назад'\n")
            if user_input in ['стоп', 'stop']:
                break
            if user_input == '1':
                file_name_1 = input("Введите название файла")
                file_path_1 = os.path.join(ROOT_DIR, 'data',
                                           file_name_1)
                if os.path.exists(file_path_1):
                    jsonworker = JSONWorker(file_path_1)
                    json_vacancies = jsonworker.load_vacancies()
                    vacancies_list = Vacancy.get_objects_list_from_objects_dict(
                        json_vacancies)
                    print('Выгрузка завершена, список с вакансиями создан')
                    continue
                else:
                    print('Выгрузка не была произведена, файла с таким'
                          ' именем в папке "data" нет')
            try:
                bool(vacancies_list)
            except NameError:
                print("Для дальнейшей работы необходимо создать список"
                      " вакансий")
                continue
            if user_input == '2':
                filter_words = input(
                    "Введите ключевые слова для фильтрации "
                    "вакансий через пробел: ").split(" ")
                vacancies_list = get_filtered_vacancies(vacancies_list,
                                                        filter_words)
                print('Вакансии отфильтрованы по ключевым словам')
            elif user_input == '3':
                min_salary = int(
                    input("Введите нижний порог заработной платы: "))
                vacancies_list = get_vacancies_by_salary(vacancies_list,
                                                         min_salary)
                print('В списке остались только вакансии с зарплатой'
                      ' выше указанной')
            elif user_input == '4':
                vacancies_list = get_sorted_vacancies(vacancies_list)
                print('Вакансии отсортированы')
            elif user_input == '5':
                top_n = int(input(
                    "Введите количество вакансий для вывода в топ N: "))
                vacancies_list = get_top_vacancies(vacancies_list,
                                                   top_n)
                print('Срез выполнен')
            elif user_input == '6':
                print_vacancies(vacancies_list)
            elif user_input == '7':
                confirm_rewrite = input('Уверены, что хотите '
                                        'перезаписать файл? д/н')
                if confirm_rewrite == 'д':
                    jsonworker.write_vacancies(vacancies_list)
                    print('Список вакансий был перезаписан в '
                          'изначальный файл')
                else:
                    print('Список вакансий не был записан')
            elif user_input == '8':
                file_name_2 = input(
                    'Введите название файла для сохранения данных')
                file_path_2 = os.path.join(ROOT_DIR, 'data',
                                           file_name_2)
                jsonworker = JSONWorker(file_path_2)
                if os.path.exists(file_path_2):
                    confirm = input(
                        'Такой файл уже есть, '
                        'желаете вести работу в нем? д/н').lower().strip()
                    if confirm == 'д':
                        confirm = input(
                            'Желаете перезаписать или дописать файл? п/д')
                        if confirm == 'д':
                            jsonworker.add_vacancies(vacancies_list)
                            print('Вакансии добавлены в файл')
                        elif confirm == 'п':
                            jsonworker.write_vacancies(vacancies_list)
                            print(
                                'Вакансии сохранены в файл с перезаписью')
                        else:
                            print('Попробуйте ввести вновь')
                else:
                    jsonworker.write_vacancies(vacancies_list)
                    print('Вакансии сохранены в файл')
            elif user_input not in ['1', '2', '3', '4', '5',
                                    '6', '7', '8', 'stop', 'стоп']:
                print('Попробуйте ввести вновь')
            else:
                print('Что-то пошло не так')


def work_with_api():
    user_input = 0
    print('В этом блоке вы можете создать запрос для api.hh.ru и в '
          'последующем выполнять манипуляции с полученной информацие\n'
          'Кнопки управления:\n'
          '1 - сделать запрос по ключевому слову\n'
          '2 - отфильтровать вакансии по ключевым словам\n'
          '3 - оставить вакансии с З/П, выше N\n'
          '4 - сортировать вакансии по убыванию минимальной З/П\n'
          '5 - оставить N вакансий от начала списка\n'
          '6 - распечатать информацию о всех вакансиях в текущем списке\n'
          '7 - сохранить текущий список вакансий в файл\n')
    while user_input != 'назад':
        if user_input in ['стоп', 'stop']:
            break
        user_input = input(
            "Что желаете сделать? Для возврата введите 'назад'\n")
        if user_input in ['стоп', 'stop']:
            break
        if user_input == '1':
            search_query = input("Введите ваш поисковый запрос")
            hh_api = HeadHunterAPI()
            hh_vacancies = hh_api.load_vacancies(search_query)
            vacancies_list = Vacancy.get_list_with_objects(hh_vacancies)
            print('Запрос выполнен, список с вакансиями создан')
            continue
        try:
            bool(vacancies_list)
        except NameError:
            print("Для дальнейшей работы необходимо создать список"
                  " вакансий")
            continue
        if user_input == '2':
            filter_words = input(
                "Введите ключевые слова для фильтрации "
                "вакансий через пробел: ").split(" ")
            vacancies_list = get_filtered_vacancies(vacancies_list,
                                                    filter_words)
            print('Вакансии отфильтрованы по ключевым словам')
        elif user_input == '3':
            min_salary = int(
                input("Введите нижний порог заработной платы: "))
            vacancies_list = get_vacancies_by_salary(vacancies_list,
                                                     min_salary)
            print('В списке остались только вакансии с зарплатой'
                  ' выше указанной')
        elif user_input == '4':
            vacancies_list = get_sorted_vacancies(vacancies_list)
            print('Вакансии отсортированы')
        elif user_input == '5':
            top_n = int(input(
                "Введите количество вакансий для вывода в топ N: "))
            vacancies_list = get_top_vacancies(vacancies_list, top_n)
            print('Срез выполнен')
        elif user_input == '6':
            print_vacancies(vacancies_list)
        elif user_input == '7':
            file_name_2 = input(
                'Введите название файла для сохранения данных')
            file_path_2 = os.path.join(ROOT_DIR, 'data', file_name_2)
            jsonworker = JSONWorker(file_path_2)
            if os.path.exists(file_path_2):
                confirm = input(
                    'Такой файл уже есть, '
                    'желаете вести работу в нем? д/н').lower().strip()
                if confirm == 'д':
                    confirm = input(
                        'Желаете перезаписать или дописать файл? п/д')
                    if confirm == 'д':
                        jsonworker.add_vacancies(vacancies_list)
                        print('Вакансии добавлены в файл')
                    elif confirm == 'п':
                        jsonworker.write_vacancies(vacancies_list)
                        print('Вакансии сохранены в файл с перезаписью')
                    else:
                        print('Попробуйте ввести вновь')
            else:
                jsonworker.write_vacancies(vacancies_list)
                print('Вакансии сохранены в файл')
        elif user_input not in ['1', '2', '3', '4', '5', '6', '7',
                                'стоп', 'stop']:
            print('Попробуйте ввести вновь')
        else:
            print('Что-то пошло не так')
    else:
        print('Попробуйте ввести вновь')
