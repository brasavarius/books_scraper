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
    None : Не ожидает параметров на входе
    Returns:
    dict : Описание тестовой книги в виде словаря
    '''
    with open("tests/test_book.txt", "r", encoding='utf-8') as fp:
        book = json.load(fp)
    return book


@pytest.fixture(name='url_book_test')
def fixture_url_book_test():
    '''
    Фикстура с загрузкой тестового url адреса книги.
    Parameters:
    None : Не ожидает параметров на входе
    Returns:
    str : Строка с url адресом книги
    '''
    with open("tests/test_url_book.txt", "r", encoding='utf-8') as fp:
        url = fp.read()
    return url


@pytest.fixture(name='url_catalogue')
def fixture_url_catalogue():
    '''
    Фикстура с тестовым url первой страницы каталога.
    Parameters:
    None : Не ожидает параметров на входе
    Returns:
    str : Строка с url адресом перовй страницы каталога
    '''
    return 'http://books.toscrape.com/catalogue/page-1.html'


def test_get_book_data(url_book_test, book_test):
    '''
    Тестирование функции получения описания книги.
    '''
    assert type(get_book_data(url_book_test)) is dict
    assert 'Title' in get_book_data(url_book_test).keys()
    assert 'Description' in get_book_data(url_book_test).keys()
    assert get_book_data(url_book_test) == book_test


def test_get_number_of_pages(url_catalogue):
    '''
    Тестирование функции получения количества страниц в каталоге.
    '''
    assert get_number_of_pages(url_catalogue) == 50


def test_get_urls_books(url_catalogue):
    '''
    Тестирование функции получения списка адресов книг на 2 страницах каталога.
    '''
    assert type(get_urls_books(url_catalogue, 2)) is list
    assert type(get_urls_books(url_catalogue, 2)[0]) is str
    assert len(get_urls_books(url_catalogue, 2)) == 40


def test_scrape_books(mocker, url_book_test, url_catalogue, book_test):
    '''
    Тестирование функции получения описания нескольких книг.
    Проверка, что функция на выходе формирует список словарей с описанием.
    Через mocker экранирован вызов функций получения количества страниц
    каталога и списка адресов книг.
    Функция тестируется на загрузке описания одной книги и формирования
    вывода в виде списка словарей.
    '''
    mocker.patch(
        'scraper.get_number_of_pages',
        return_value=2
    )
    mocker.patch(
        'scraper.get_urls_books',
        return_value=[url_book_test, ]
    )
    assert type(scrape_books(is_save=False, url=url_catalogue)) is list
    assert type(scrape_books(is_save=False, url=url_catalogue)[0]) is dict
    assert scrape_books(is_save=False, url=url_catalogue) == [book_test,]
