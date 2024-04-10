import os
import pathlib

from config import ROOT_DIR
from src.headhunterapi import HeadHunterAPI
from src.jsonworker import JSONWorker
from src.utils import get_filtered_vacancies, print_vacancies, \
    get_top_vacancies, get_sorted_vacancies, get_vacancies_by_salary
from src.vacancy import Vacancy


def main():
    print("Доброго времени суток, вы запустили программу "
          "для упрощенного общения с вакансиями")
    user_input = ''
    while user_input not in ['стоп', 'stop']:
        user_input = input(
            'Если желаете работать с вакансиями из файлов введите - 1\n'
            'Если желаете работать с вакансиями, получаемыми с api.hh.ru - 2\n').lower().strip()
        if user_input == '1':
            while user_input != 'назад':
                pass
        elif user_input == '2':
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
                elif user_input == '2':
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
                    file_name = input(
                        'Введите название файла для сохранения данных')
                    file_path = os.path.join(ROOT_DIR, 'data', file_name)
                    jsonsaver = JSONWorker(file_path)
                    if os.path.exists(file_path):
                        confirm = input(
                            'Такой файл уже есть, '
                            'желаете вести работу в нем? д/н').lower().strip()
                        if confirm == 'д':
                            confirm = input(
                                'Желаете перезаписать или дописать файл? п/д')
                            if confirm == 'д':
                                jsonsaver.add_vacancies(vacancies_list)
                                print('Вакансии добавлены в файл')
                            elif confirm == 'п':
                                jsonsaver.write_vacancies(vacancies_list)
                                print('Вакансии сохранены в файл с перезаписью')
                            else:
                                print('Попробуйте ввести вновь')
                    else:
                        jsonsaver.write_vacancies(vacancies_list)
                        print('Вакансии сохранены в файл')
                else:
                    print('Попробуйте ввести вновь')

        else:
            print('Попробуйте ввести вновь')


if __name__ == "__main__":
    main()
