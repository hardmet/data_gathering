"""
ЗАДАНИЕ

Выбрать источник данных и собрать данные по некоторой предметной области.

Цель задания - отработать навык написания программ на Python.
В процессе выполнения задания затронем области:
- организация кода в виде проекта, импортирование модулей внутри проекта
- unit тестирование
- работа с файлами
- работа с протоколом http
- работа с pandas
- логирование

Требования к выполнению задания:

- собрать не менее 1000 объектов

- в каждом объекте должно быть не менее 5 атрибутов
(иначе просто будет не с чем работать.
исключение - вы абсолютно уверены что 4 атрибута в ваших данных
невероятно интересны)

- сохранить объекты в виде csv файла

- считать статистику по собранным объектам


Этапы:

1. Выбрать источник данных.

Это может быть любой сайт или любое API

Примеры:
- Пользователи vk.com (API)
- Посты любой популярной группы vk.com (API)
- Фильмы с Кинопоиска
(см. ссылку на статью выше)
- Отзывы с Кинопоиска
- Статьи Википедии
(довольно сложная задача,
можно скачать дамп википедии и распарсить его,
можно найти упрощенные дампы)
- Статьи на habrahabr.ru
- Объекты на внутриигровом рынке на каком-нибудь сервере WOW (API)
(желательно англоязычном, иначе будет сложно разобраться)
- Матчи в DOTA (API)
- Сайт с кулинарными рецептами
- Ebay (API)
- Amazon (API)
...

Не ограничивайте свою фантазию. Это могут быть любые данные,
связанные с вашим хобби, работой, данные любой тематики.
Задание специально ставится в открытой форме.
У такого подхода две цели -
развить способность смотреть на задачу широко,
пополнить ваше портфолио (вы вполне можете в какой-то момент
развить этот проект в стартап, почему бы и нет,
а так же написать статью на хабр(!) или в личный блог.
Чем больше у вас таких активностей, тем ценнее ваша кандидатура на рынке)

2. Собрать данные из источника и сохранить себе в любом виде,
который потом сможете преобразовать

Можно сохранять страницы сайта в виде отдельных файлов.
Можно сразу доставать нужную информацию.
Главное - постараться не обращаться по http за одними и теми же данными много раз.
Суть в том, чтобы скачать данные себе, чтобы потом их можно было как угодно обработать.
В случае, если обработать захочется иначе - данные не надо собирать заново.
Нужно соблюдать "этикет", не пытаться заддосить сайт собирая данные в несколько потоков,
иногда может понадобиться дополнительная авторизация.

В случае с ограничениями api можно использовать time.sleep(seconds),
чтобы сделать задержку между запросами

3. Преобразовать данные из собранного вида в табличный вид.

Нужно достать из сырых данных ту самую информацию, которую считаете ценной
и сохранить в табличном формате - csv отлично для этого подходит

4. Посчитать статистики в данных
Требование - использовать pandas (мы ведь еще отрабатываем навык использования инструментария)
То, что считаете важным и хотели бы о данных узнать.

Критерий сдачи задания - собраны данные по не менее чем 1000 объектам (больше - лучше),
при запуске кода командой "python3 -m gathering stats" из собранных данных
считается и печатается в консоль некоторая статистика

Код можно менять любым удобным образом
Можно использовать и Python 2.7, и 3

"""

import logging

import sys

from parsers.html_parser import HtmlParser
from scrappers.scrapper import Scrapper
from storages.file_storage import FileStorage
import pandas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SCRAPPED_FILE = 'scrapped_data.txt'
TABLE_FORMAT_FILE = 'data.csv'


def gather_process():
    logger.info("gather")
    storage = FileStorage(SCRAPPED_FILE)

    # You can also pass a storage
    scrapper = Scrapper()
    scrapper.scrap_process(storage)


def convert_data_to_table_format():
    logger.info("transform")

    # Your code here
    # transform gathered data from txt file to pandas DataFrame and save as csv
    storage = FileStorage(SCRAPPED_FILE)
    text_data = ''
    for i in storage.read_data():
        text_data += i

    parser = HtmlParser(['model', 'date', 'size', 'standard-price', 'promo-price', 'color'])
    parsed_data = parser.parse(text_data)
    df = pandas.DataFrame(parsed_data)
    df.to_csv(TABLE_FORMAT_FILE, sep='\t', encoding='utf-8')


def stats_of_data():
    logger.info("stats")
    # Your code here
    # Load pandas DataFrame and print to stdout different statistics about the data.
    # Try to think about the data and use not only describe and info.
    # Ask yourself what would you like to know about this data (most frequent word, or something else)
    goods = pandas.read_csv(TABLE_FORMAT_FILE, sep='\t')
    print('goods count: ' + str(len(goods)))
    print('rarest size: ' + goods['size'].value_counts().idxmin())
    goods_for_prices = goods
    goods_for_prices['standard-price'] = goods_for_prices['standard-price']
    max_value = goods_for_prices.loc[goods_for_prices['standard-price'].idxmax()]['standard-price']
    print('max standard-price: ' + str(max_value))
    print('goods with max standard-price: ' + str(len(goods_for_prices[goods_for_prices['standard-price'].apply(lambda x: x == max_value)])))
    goods['diff'] = goods['standard-price'] - goods['promo-price']
    max_value = goods.loc[goods['diff'].idxmax()]['diff']
    goods_with_max_diff = goods[goods['diff'].apply(lambda x: x == max_value)]
    print('goods with maximum difference between standard-price and promo-price: ')
    print(goods_with_max_diff)
    goods = goods.drop(columns=['diff'], axis=1)
    goods['DateTime'] = goods['date'].apply(lambda x: pandas.to_datetime(str(x), format='%Y%m%d'))
    print('trend color in 2018: ' + goods[goods['DateTime'] >= '2018-01-01']['color'].value_counts().idxmax())
    print('trend color in 2017: ' + goods[(goods['DateTime'] >= '2017-01-01') & (goods['DateTime'] < '2018-01-01')]['color'].value_counts().idxmax())

if __name__ == '__main__':
    """
    why main is so...?
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    elif sys.argv[1] == 'stats':
        stats_of_data()

    logger.info("work ended")
