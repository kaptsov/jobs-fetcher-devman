import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


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


def fetch_headhunter(lang_collection):

    language_salaries = {}

    for lang in lang_collection:

        ave_salary = 0
        page = 0
        pages_amount = 1
        per_page = 100

        while page < pages_amount:
            vacancy_search_field = {
                'text': f'программист {lang}',
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
            pages_amount = response.json()['pages']
            vacancies_found = int(response.json()['found'])

            for vacancy in response.json()['items']:
                if vacancy['salary'] and predict_rub_salary_hh(vacancy):
                    ave_salary += predict_rub_salary_hh(vacancy)
            page += 1
        if vacancies_found > 2000:
            vacancies_processed = pages_amount * per_page
        else:
            vacancies_processed = vacancies_found

        ave_salary = int(ave_salary / vacancies_processed)

        language_salaries[lang] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': ave_salary,
        }

    print_table(language_salaries, 'HeadHunter')


def fetch_superjob(lang_collection):

    superjob_token = os.getenv("SUPERJOB_SECRET_KEY")
    count = 100
    language_salaries_sj = {}

    headers = {
        'X-Api-App-Id': superjob_token,
    }
    for lang in lang_collection:

        ave_salary = 0
        min_sal = 10000000
        max_sal = 0
        page = 0
        pages_amount = 1

        while page < pages_amount:

            params = {
                'keywords': f'Программист {lang}',
                'town': 'Москва',
                'no_agreement': 1,
                'payment_from': 70000,
                'count': count
            }
            response = requests.get(f'https://api.superjob.ru/2.2/vacancies/',
                                    headers=headers, params=params)
            response.raise_for_status()

            vacancies_found = int(response.json()['total'])
            pages_amount = int(vacancies_found / count + 1)

            for vacancy in response.json()['objects']:
                if predict_rub_salary_sj(vacancy):
                    ave_salary += predict_rub_salary_sj(vacancy)
            page += 1

        if vacancies_found > 2000:
            vacancies_processed = pages_amount * count
        else:
            vacancies_processed = vacancies_found

        ave_salary = int(ave_salary / vacancies_processed)

        language_salaries_sj[lang] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': ave_salary
        }

    print_table(language_salaries_sj, 'SuperJob')


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
        table_data += (name, info['vacancies_found'],
                       info['vacancies_processed'],
                       info['average_salary']),
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)


if __name__ == '__main__':

    load_dotenv()
    lang_collection = os.getenv('LANGUAGE_COLLECTION').split(', ')

    fetch_superjob(lang_collection)
    fetch_headhunter(lang_collection)
