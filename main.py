import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable
from itertools import count


def predict_salary(salary_from, salary_to):

    if not salary_from and salary_to:
        return salary_to * 0.8
    elif not salary_to and salary_from:
        return salary_from * 1.2

    return (salary_from + salary_to) / 2


def predict_rub_salary_sj(vacancy):

    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    salary_currency = vacancy['currency']
    if salary_currency == 'rub':
        return predict_salary(salary_from, salary_to)


def predict_rub_salary_hh(vacancy):

    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']
    salary_currency = vacancy['salary']['currency']
    if salary_currency == 'RUR':
        return predict_salary(salary_from, salary_to)


def get_headhunter_vacancy(language):

    average_salary = 0
    per_page = 100

    for page in count(0, 1):
        vacancy_search_field = {
            'text': f'программист {language}',
            'area': 1,
            'date_from': '2022-02-01',
            'per_page': per_page,
            'page': page,
            'only_with_salary': True,
            'salary': 70000,

        }
        response = requests.get('https://api.hh.ru/vacancies',
                                params=vacancy_search_field)
        response.raise_for_status()
        response_json = response.json()
        pages_amount = response_json['pages']
        vacancies_found = int(response_json['found'])

        for vacancy in response_json['items']:
            if vacancy['salary'] and predict_rub_salary_hh(vacancy):
                average_salary += predict_rub_salary_hh(vacancy)
        if page > pages_amount:
            break

    if vacancies_found > 2000:
        vacancies_processed = pages_amount * per_page
    else:
        vacancies_processed = vacancies_found

    average_salary = int(average_salary / vacancies_processed)

    return vacancies_found, vacancies_processed, average_salary


def get_superjob_vacancy(language, superjob_token):

    page_count = 100

    headers = {
        'X-Api-App-Id': superjob_token,
    }

    average_salary = 0

    for page in count(0, 1):

        params = {
            'keywords': f'Программист {language}',
            'town': 'Москва',
            'no_agreement': 1,
            'payment_from': 70000,
            'count': page_count
        }
        response = requests.get(f'https://api.superjob.ru/2.2/vacancies/',
                                headers=headers, params=params)
        response.raise_for_status()
        response_json = response.json()
        vacancies_found = int(response_json['total'])
        pages_amount = int(vacancies_found / page_count + 1)

        for vacancy in response.json()['objects']:
            if predict_rub_salary_sj(vacancy):
                average_salary += predict_rub_salary_sj(vacancy)
        if page > pages_amount:
            break

    if vacancies_found > 2000:
        vacancies_processed = pages_amount * page_count
    else:
        vacancies_processed = vacancies_found

    average_salary = int(average_salary / vacancies_processed)

    return vacancies_found, vacancies_processed, average_salary


def print_table(stat_by_language, title):
    table_data = (
        (
            'Язык программирования',
            'Найдено вакансий',
            'Вакансий обработано',
            'Средняя зарплата'
        ),
    )
    for name, info in stat_by_language.items():
        table_data += (name, info[0],
                       info[1],
                       info[2]),
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)


if __name__ == '__main__':

    load_dotenv()
    lang_collection = os.getenv('LANGUAGE_COLLECTION').split(', ')
    superjob_token = os.getenv("SUPERJOB_SECRET_KEY")
    language_salaries_hh = {}
    language_salaries_sj = {}

    print('Выполняется поиск... Может занять около нескольких минут...')
    for language in lang_collection:
        language_salaries_hh[language] = get_headhunter_vacancy(language)
        language_salaries_sj[language] = get_superjob_vacancy(
            language,
            superjob_token
            )

    print_table(language_salaries_hh, 'HeadHunter')
    print_table(language_salaries_sj,  'SuperJob')
