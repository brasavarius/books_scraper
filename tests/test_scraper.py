"""
Модуль тестирования логики scraper.py
"""
import json

import pytest

from scraper import (
    get_book_data, get_number_of_pages, get_urls_books, scrape_books
)


@pytest.fixture(name='book_test')
def fixture_book_test():
    '''
    Фикстура с загрузкой описания тестовой книги из файла.
    Parameters:
    name (str): Отображаемое имя функции для использования в тесте
    Returns:
    dict: Описание тестовой книги в виде словаря
    '''
    with open("tests/test_book.txt", "r", encoding='utf-8') as fp:
        book = json.load(fp)
    return book


@pytest.fixture(name='url_book_test')
def fixture_url_book_test():
    '''
    Фикстура с загрузкой тестового url адреса книги.
    Parameters:
    name (str): Отображаемое имя функции для использования в тесте
    Returns:
    str: Строка с url адресом книги
    '''
    with open("tests/test_url_book.txt", "r", encoding='utf-8') as fp:
        url = fp.read()
    return url


@pytest.fixture(name='url_catalogue')
def fixture_url_catalogue():
    '''
    Фикстура с тестовым url первой страницы каталога.
    Parameters:
    name (str): Отображаемое имя функции для использования в тесте
    Returns:
    str: Строка с url адресом перовй страницы каталога
    '''
    return 'http://books.toscrape.com/catalogue/page-1.html'


def test_get_book_data(url_book_test, book_test):
    '''
    Тестирование функции получения описания книги.
    Parameters:
    url_book_test (str): Адрес сайта для проверки работы парсинга
    book_test (dict): Словарь с тестовым описанием книги
    Returns:
    None: Не ожидается возврата значений (только инициация assert)
    '''
    # Проверка что описание книги выдается словарем
    assert isinstance(get_book_data(url_book_test), dict)
    # Проверка, что в описании книги есть требуемые по заданию поля
    keys = [
        'Title', 'Description', 'Price (incl. tax)',
        'Rating', 'Availability'
    ]
    for key in keys:
        assert key in get_book_data(url_book_test)
    # Проверка соответствия получаемого описания книги с ожидаемым
    assert get_book_data(url_book_test) == book_test


def test_get_number_of_pages(url_catalogue):
    '''
    Тестирование функции получения количества страниц в каталоге.
    Parameters:
    url_catalogue (str): Адрес каталога для проверки количества страниц
    Returns:
    None: Не ожидается возврата значений (только инициация assert)
    '''
    assert get_number_of_pages(url_catalogue) == 50


def test_get_urls_books(url_catalogue):
    '''
    Тестирование функции получения списка адресов книг на 2 страницах каталога.
    Parameters:
    url_catalogue (str): Адрес каталога для проверки парсинга каталога
    Returns:
    None: Не ожидается возврата значений (только инициация assert)
    '''
    # Проверяем, что адреса книг выдаются списком
    assert isinstance(get_urls_books(url_catalogue, 2), list)
    # Проверяем, что адрес отдельной книги выдается строкой
    assert isinstance(get_urls_books(url_catalogue, 2)[0], str)
    # Проверяем на примере 2-х страниц каталога, что находит все 20 книг на
    # каждой странице каталога
    assert len(get_urls_books(url_catalogue, 2)) == 40


def test_scrape_books(mocker, url_book_test, url_catalogue, book_test):
    '''
    Тестирование функции получения описания нескольких книг.
    Проверка, что функция на выходе формирует список словарей с описанием.
    Через mocker экранирован вызов функций получения количества страниц
    каталога и списка адресов книг.
    Функция тестируется на загрузке описания одной книги и формирования
    вывода в виде списка словарей.
    Parameters:
    moker (mock_class): Декоратор функций (для подмены вызываемых функций)
    url_book_test (str): Адрес сайта для подмены выдачи внутренней функции
    url_catalogue (str): Адрес каталога для проверки парсинга каталога книг
    book_test (dict): Словарь с тестовым описанием книги
    Returns:
    None: Не ожидается возврата значений (только инициация assert)
    '''
    # Подменяем вывод функции get_number_of_pages, чтобы не тратить дополни-
    # тельное время на парсинг количества страниц + сокращаем количество
    # проходов до 2-х страниц каталога
    mocker.patch(
        'scraper.get_number_of_pages',
        return_value=2
    )
    # Подменяем вызов функции get_urls_books, чтобы не тратить дополнительное
    # время на парсинг адресов книг в каталоге + выдаем список из адресов
    # только на одну книгу, для сокращения времени тестирования
    mocker.patch(
        'scraper.get_urls_books',
        return_value=[url_book_test, ]
    )
    # Проверка, что информация о книгах выдается списком
    assert isinstance(scrape_books(is_save=False, url=url_catalogue), list)
    # Проверка, что список информации о книгах состоит из словарей по каждой
    # конкретной книге.
    assert isinstance(scrape_books(is_save=False, url=url_catalogue)[0], dict)
    # Проверка, что описание конкретной книги соответстует ожидаемому
    assert scrape_books(is_save=False, url=url_catalogue) == [book_test,]
