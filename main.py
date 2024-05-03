from src.utils import work_with_file, work_with_api


def main():
    print("Доброго времени суток, вы запустили программу "
          "для упрощенного общения с вакансиями")
    user_input = ''
    while user_input not in ['стоп', 'stop']:
        user_input = input(
            'Если желаете работать с вакансиями из файлов введите - 1\n'
            'Если желаете работать с вакансиями, получаемыми с api.hh.ru - 2\n').lower().strip()
        if user_input == '1':
            work_with_file()
        elif user_input == '2':
            work_with_api()
        else:
            print('Выберите режим работы из предложенных')


if __name__ == "__main__":
    main()
