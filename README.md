# Средние зарплаты программистов

Анализ зарплат программистов в Москве в зависимости от ЯП.

## Как установить

Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей.

`pip install -r requirements.txt`

## Файл конфигурации

Создайте в папке с проектом файл ".env"
и положите в него следующие значения:

```
SUPERJOB_SECRET_KEY={API SUPERJOB KEY}

LANGUAGE_COLLECTION='python, C++, JavaScript, Java, Ruby, PHP, C#'
```

Как получить токен от API сайта superjob описану [по ссылке](https://api.superjob.ru/#access_token)

## Пример использования

`python main.py`

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Dvmn.org](https://dvmn.org/modules/).

# Average salaries of programmers

Analysis of the salaries in RUB of programmers in Moscow depending on the programming language.

## How to install

Python3 should already be installed. Then use `pip` (or `pip3`, there is a conflict with Python2) to install the dependencies.

`pip install -r requirements.txt`

## Configuration file

Create a ".env" file in the project folder
and put the following values ​​into it:

```
SUPERJOB_SECRET_KEY={API SUPERJOB KEY}

LANGUAGE_COLLECTION='python, C++, JavaScript, Java, Ruby, PHP, C#'
```

How to get a token from the superjob site API is described [link](https://api.superjob.ru/#access_token)

## Usage example

`python main.py`

## Objective of the project
The code was written for educational purposes in the online course for web developers [Dvmn.org](https://dvmn.org/modules/).