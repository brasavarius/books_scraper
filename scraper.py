'''
Модуль для парсинга каталога книг и сбора по ним информации в список словарей.
'''
import json
import re
import time
from typing import Dict, List

from bs4 import BeautifulSoup

import requests

import schedule

from tqdm import tqdm


# Адрес первой страницы каталога книг
URL = 'http://books.toscrape.com/catalogue/page-1.html'


def get_book_data(book_url: str) -> dict:
    '''
    Сбор данных о книге с одной страницы парсингом.
    Parameters:
    book_url (str): Адрес страницы для парсинга.
    Returns:
    dict: Собранные данные о книге.
    '''

    # Получаем страницу по ардесу book_url
    responce = requests.get(book_url, timeout=5)
    # Словарь для вывода данных по результатам работы функции
    res: dict = {}
    # Убеждаемся, что наш запрос отработал корректно и вернул код состояния 200
    if responce.status_code != 200:
        raise ConnectionError(f"Can't connect to {responce.status_code}")
    # Разбираем парсером bs4 полученный в запросе текст
    soup: BeautifulSoup = BeautifulSoup(responce.text, 'html.parser')
    # Находим название книги по ближайшему уникальному тегу и его атрибуту
    tag_name = soup.find('div', attrs={'class': 'col-sm-6 product_main', })
    try:
        # Добавляем название книги в словарь вывода с ключем Name
        res['Title'] = tag_name.h1.text
    except AttributeError:
        res['Title'] = "Нет описания имени книги на сайте"
    # Находим описание книги по соседнему уникальному тегу и его атрибуту
    sibling = soup.find('div', attrs={'id': 'product_description', })
    try:
        res['Description'] = sibling.find_next_sibling().text
    except AttributeError:
        res['Description'] = 'Нет описания на сайте'
    # Находим по тегу и его уникальному атрибуту таблицу с остальными
    # характеристиками книги. Через children получаем итератор по вложенным
    # тегам.
    table_inf = soup.find('table', attrs={'class': 'table table-striped'})
    if table_inf:
        product_inf = table_inf.children
        # Проходим в цикле по итератору
        for row in product_inf:
            # В тегах, кроме искомых th - название характеристики и
            # td - значение характеристики, есть еще мешающий тег tr
            # его обрабатываем try/except (обеспечение консистентности).
            try:
                # Через пары th:td (название:значение) дополняем словарь вывода
                res[row.th.text] = row.td.text
            except AttributeError:
                pass
    return res


def get_number_of_pages(url: str) -> int:
    '''
    Получение количества страниц каталога по первой странице в каталоге.
    Parameters:
    url (str): Строка с адресом первой страницы в каталоге
    Returns:
    int: Количество страниц в каталоге
    '''
    responce = requests.get(url, timeout=5)
    # Проверяем, что страница доступна
    if responce.status_code != 200:
        raise ConnectionError(f"Can't connect to {responce.status_code}")
    # Проходим парсингом bs4 по полученной странице
    soup = BeautifulSoup(responce.text, 'html.parser')
    # Находим поле, описывающее количество страниц в каталоге
    current_page = soup.find('li', attrs={'class': 'current'})
    # Пытаемся извлечь текст количества страниц в каталоге, преобразуем в int
    try:
        number_of_pages = int(current_page.text.split()[-1])
    except AttributeError:
        pass
    return number_of_pages


def get_urls_books(url: str, number_of_pages: int) -> List[str]:
    '''
    Получение url всех книг в каталоге
    Parameters:
    url (str): Строка с адресом первой страницы в каталоге
    number_of_pages (int): Количество страниц в каталоге
    Returns:
    list(str): Список url всех книг в каталоге
    '''

    # Пустой список, для наполнения строками адресов книг
    urls = []
    # Проходим циклом по каждой странице каталога
    for i in range(1, number_of_pages+1):
        # Не меняющаяся часть url + номер страницы каталога
        url_p = f'{re.search('.+page-', url)[0]}{str(i)}.html'
        # Проверка на доступность страницы каталога
        resp_book = requests.get(url_p, timeout=5)
        if resp_book.status_code != 200:
            raise ConnectionError(f"Can't connect to {resp_book.status_code}")
        # Проходим парсингом bs4 по странице каталога
        soup_book = BeautifulSoup(resp_book.text, 'html.parser')
        pattern = r'.+catalogue/'
        # Формируем список url, используя не меняющуюся часть url каталога,
        # добавляем к нему относительный адрес книги, найденный в атрибуте
        # href=... списка тегов книг <a href=....>...</a>
        # Список ссылок формируем накоплением.
        urls += list(
            map(
                lambda s: f'{re.search(pattern, url)[0]}{s.a.attrs['href']}',
                soup_book.find('ol', class_='row').find_all('h3')
            )
        )
    return urls


def scrape_books(is_save: bool, url: str) -> List[Dict]:
    '''
    Проход в цикле по страницам каталога, с парсингом всех страниц,
    с использованием функции get_book_data.
    Parameters:
    is_save (bool): Осуществлять ли запись в файл.
    url (string): URL адрес первой страницы в каталоге
    Returns:
    list(dict,): Собранные данные о книге.
    '''

    list_return = []
    number_of_pages = get_number_of_pages(url)
    urls = get_urls_books(url, number_of_pages)
    # Проход циклом по списку ссылок на книги, вызывая get_book_data для каждой
    for url_b in tqdm(urls):
        list_return.append(get_book_data(url_b))
    # Сохраняем собранную информацию в файл, если задан соответствующий ключ
    if is_save:
        with open('artifacts//books_data.txt', 'w', encoding='utf-8') as file:
            # Записываем данные о книгах построчно
            # В каждой новой строке словарь данных по новой книге
            for res_dict in list_return:
                json.dump(res_dict, file)
    return list_return


if __name__ == '__main__':
    schedule.every().day.at("19:00").do(lambda: scrape_books(
        is_save=True, url=URL
        )
    )
    while True:
        schedule.run_pending()
        time.sleep(1)
