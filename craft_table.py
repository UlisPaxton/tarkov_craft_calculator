# -*- coding: UTF-8 -*-

from sys import exit
import browser
import json


class JSONDataSource:
    def __init__(self, data_source_string):
        """

        :param data_source_string: путь к файлу json
        """
        self.json_file_path = data_source_string

    def save(self, data_to_save):

        with open(self.json_file_path, 'w', encoding="utf-8") as fd:
            json.dump(data_to_save, fd, ensure_ascii=False)

    def load(self):

        with open(self.json_file_path, encoding="utf-8") as json_file:
            json_table = json.load(json_file)
        return json_table


class Craft:

    CRAFT_TABLE_FILE = 'craft_table.json'
    browser = browser.InterfaceCacher(browser.CustomBrowser)
    """Первое, что приходит на ум - сделать craft_table - словарём, но такой подход косячен, 
    поскольку одни и те же предметы могут быть изготовлены из разных наборов ресурсов, craft_table как словарь вынуждает
    обрабатывать предметы в цыкле, но при этом позволяет использовать дублирующие наборы ингридиентов"""
    json_reader = JSONDataSource(CRAFT_TABLE_FILE)
    craft_table = json_reader.load()

    @classmethod
    def get(cls, item_name: str):
        try:
            return cls.name_matching_table[item_name]
        except KeyError:
            return item_name

    @classmethod
    def get_craft_element(cls, item_name: str):
        for element in cls.craft_table:
            if element['name'] == item_name:
                return element

        print(item_name, "нет в таблице крафта.")
        exit()

    @classmethod
    def add(cls, name: str, market_name: str, craft_from: list, result_count: int, craft_duration: int):

        """Добавление структуры в таблицу крафта
        пример вызова
        add('Магазин 6Л31', 'Магазин 6Л31', [*repeat('Магазин 6Л23', 4), 'Липкая лента KEKТЕЙП'], 1, 80)
        результат
        {'name': 'Магазин 6Л31',

         'craft_from': ['Магазин 6Л23', 'Магазин 6Л23', 'Магазин 6Л23',
                        'Магазин 6Л23', 'Липкая лента KEKТЕЙП'],
         'result_count': 1,
        'craft_duration': 80}

        параметр market_name предназначен для подстанвки в поисковый запрос в качестве точного указателя
         в соответствии с API и не всегда является удобочитаемым
         ВАЖНО!!!
         Такая структура данных позволяет описывать процесс крафта какого-либо предмета включая крафт его ингредиентов,
         для корректного рассчёта нужно в параметр craft_from передать список, суммированный из списков крафта
         ингридиентов, так же нужно учитывать сумарное время и добавлять некоторый интервал(1-2 минуты) на сбор
         результатов крафта вторичных предметов и запуск первичного процесса крафта.
        """

        cls.craft_table.append({'name': name, 'market_name': market_name, 'craft_from': craft_from, 'result_count': result_count,
                                'craft_duration': craft_duration})

    @classmethod
    def craft(cls, item_name: str):
        item = cls.get_craft_element(item_name)

        item_market_name = item['market_name']
        
        item_sale_price = cls.browser.get_price(item_market_name)
        result_sale_price = item_sale_price * item['result_count']
        total_price = 0

        print('---------------------------------------------------------')
        resource_prices_dict = {}
        for resource in item['craft_from']:
            resource_price = cls.browser.get_price(cls.get(resource))
            resource_prices_dict.update({resource: resource_price})

            total_price += resource_price

        print('Крафтим', item['name'])
        print('Цена продажи:', result_sale_price, 'Цена ресурсов:', total_price)
        print('При цене ингредиентов:')
        for resource in resource_prices_dict.keys():
            print('    ', resource, ':', resource_prices_dict[resource])
        print('Профит:', result_sale_price - total_price)
        print('Профит в час', (result_sale_price - total_price)/item['craft_duration'] * 60)
        print('Время крафта:', item['craft_duration'] / 60, 'часов.')


