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