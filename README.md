#  Парсер данных книг с сайта [Books to Scrape](http://books.toscrape.com)

## Описание проекта

Cистема для автоматического сбора данных о книгах с сайта [Books to Scrape](http://books.toscrape.com).
Реализованы функции:
* для парсинга всех страниц сайта
* извлечения информации о книгах
* автоматического ежедневного запуска задачи
* сохранения результата.

## Как запустить проект у себя, используя исходный код с GitHub:

1. Склонируйте репозитарий и перейдите в каталог проекта:
```
git clone git@github.com:brasavarius/books_scraper.git
cd books_scraper
```
2. Создайте в том же каталоге виртуальное окружение и активируйте его (вариант для unix систем):
```
python3 -m venv .venv
source .venv/bin/activate
```
3. Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. Запустите проект в виртуальном окружении:
```
python scraper.py
```
Процесс длительный, зависит от скорости подключения к интернету. Выполнение сопровождается прогресс баром в консоли.


## Используемые библиотеки
| Lib | Link| For why in this project |
| ------ | ------ | ------ |
| json | https://docs.python.org/3/library/json.html | Encoding and Decoding dict in txt file |
| re | https://docs.python.org/3/library/re.html | Regular expression for extract information from string |
| time | https://docs.python.org/3/library/time.html | To pause the execution of the start time check in an infinite loop |
| typing | https://docs.python.org/3/library/typing.html | For type hints like List[Dict] |
| bs4 | https://beautiful-soup-4.readthedocs.io/en/latest/ | For pulling data out of HTML |
| requests | https://requests.readthedocs.io/en/latest/index.html | For getting html from the WEB |
| schedule | https://schedule.readthedocs.io/en/stable/index.html |  For job scheduling 19:00 every day |

## Автор:

Леденев Виктор.

## License

MIT
