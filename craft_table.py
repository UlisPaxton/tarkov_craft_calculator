from sys import exit
import browser



def repeat(item_name: str, count: int):
    """мультиплексор, возвращает словарь строк item_name, содержащий count элементов"""
    generated_list = [item_name] * count
    return generated_list


class Craft:
    browser = browser.CustomBrowser()
    """Первое, что приходит на ум - сделать craft_table - словарём, но такой подход косячен, 
    поскольку одни и те же предметы могут быть изготовлены из разных наборов ресурсов, craft_table как словарь вынуждает
    обрабатывать предметы в цыкле, но при этом позволяет использовать дублирующие наборы ингридиентов"""
    craft_table = [{'name': 'Кейс для магазинов',

                    'craft_from': [*repeat('Канистра Экспедиционная топливная 0/60', 2), *repeat('Болты', 3),
                                   *repeat('Гайки', 3), 'Ножницы для резки металла'
                                   ],
                    'result_count': 1,
                    'craft_duration': 283,
                    }
                   ]
    name_matching_table = {'Канистра Экспедиционная топливная (0/60)': 'Expeditionary fuel tank (0/60)'}
    """словарь name_matching_table нужен чтобы сопоставить кастомное наименование предмета с наименованием из 
    JSON-ответа tarkov-market. Что бы понять проблему найдите предмет 'Печатная плата' и вы увидите в 
    поиске 2 результата - Печатную плату и военную микросхему, несмотря на такой ляп поиска, бэк-енд tarkov-market
    возвращает для каждого из этих предметов разные англоязычные имена API.
    В принципе можно задать любое имя в качестве ключа словаря name_matching_table, это очень хорошо подходит
    для описания крафта печатных плат из газоанализатора и отвёртки и из DVD и плоской отвёртки."""

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

        cls.craft_table.append({'name': name, 'craft_from': craft_from, 'result_count': result_count,
                                'craft_duration': craft_duration})
        cls.name_matching_table.update({name: market_name})

    @classmethod
    def craft(cls, item_name: str):
        item = cls.get_craft_element(item_name)

        try:

            item_market_name = cls.name_matching_table[item['name']]
        except KeyError:
            item_market_name = item['name']

        item_sale_price = cls.browser.get_price(item_market_name)
        result_sale_price = item_sale_price * item['result_count']
        total_price = 0

        print('---------------------------------------------------------')
        for resource in item['craft_from']:
            resource_price = cls.browser.get_price(cls.get(resource))

            total_price += resource_price

        print('Крафтим', item['name'])
        print('Цена продажи:', result_sale_price, 'Цена ресурсов:', total_price)
        print('Профит:', result_sale_price - total_price)
        print('Профит в час', (result_sale_price - total_price)/item['craft_duration'] * 60)
