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


# ----------------------- наполнение таблицы крафта
# ----------------------- санузел
Craft.add('Водный фильтр', 'Water filter', [*repeat('Воздушный фильтр для противогаза', 4),
                                            'Ножницы для резки металла', 'Бумага для принтера'], 1, 571)
Craft.add('Бронежилет модуль 3М', 'Module-3M bodyarmor (40/40)', [*repeat('Арамидная ткань', 2),
                                                                  *repeat('Ткань рипстоп', 2)], 1, 52)
Craft.add('Кейс для Хлама', 'Lucky Scav Junkbox', [*repeat('Кейс для магазинов', 3), *repeat('Болты', 6),
                                                   *repeat('Липкая лента KEKТЕЙП', 3),
                                                   'Ножницы для резки мателла'], 1, 657)
Craft.add('Канистра Экспедиционная топливная (60/60)', 'Expeditionary fuel tank (60/60)',
          [*repeat('Бензиновая зажигалка Zibbo', 10), *repeat('Зажигалка Crickent', 10)], 1, 59)
Craft.add('Рулон туалетной бумаги', 'Toilet paper', [*repeat('Бумага для принтера', 2)], 2, 25)
Craft.add('Отбеливатель', 'Ox bleach', ['Кусок мыла', 'Средство для промывки теплообменных поверхностей',
                                        'Пачка соды'], 5, 37)
Craft.add('Воздушный фильтр для противогаза', 'Air filter for gas mask', ['Противогаз ГП-5'], 1, 1)
Craft.add('Арамидная ткань', 'Aramid fiber cloth', ['Бронежилет PACA Soft Armor'], 2, 32)
Craft.add('Алюминиевая шина для переломов', 'Immobilizing splint (alu)', ['Бронежилет MF-UNTAR (0/45)',
                                                                          'Ножницы для резки металла'], 2, 51)
Craft.add('Ткань рипстоп', 'Ripstop cloth', [*repeat('Жилет дикого', 3)], 2, 35)
Craft.add('Магазин 6Л31', 'Магазин 6Л31', [*repeat('Магазин 6Л23', 4), 'Липкая лента KEKТЕЙП'], 1, 80)

Craft.add('Разгрузочный жилет BlackRock chest rig', 'BlackRock chest rig',
          ['Разгрузочный жилет Сплав Тарзан М22', 'Ткань рипстоп', 'Полиамидная ткань Кордура'], 1, 57)
Craft.add('Кейс для гранат', 'Grenade case', [*repeat('Канистра Металлическая топливная (0/100)', 2),
                                              *repeat('Гайки', 5),
                                              *repeat('Болты', 5),
                                              'Ножницы для резки металла', 'Гаечный ключ'], 1, 962)
Craft.add('Бронежилет PACA Soft Armor', 'PACA Soft Armor (50/50)', [*repeat('Арамидная ткань', 3),
                                                                    *repeat('Ткань рипстоп', 2)], 1, 70)
Craft.add('Бутылка шампуня Schaman', 'Schaman shampoo', ['Кусок мыла', 'Бутылка воды 0.6 л'], 2, 33)
Craft.add('Рюкзак Дикого', 'Scav Backpack', ['Флисовая ткань', 'Ткань рипстоп'], 2, 52)
Craft.add('WD-40 100мл', 'WD-40 100ml.', ['WD-40 400мл', 'Ножницы для резки металла'], 2, 144)
Craft.add('Бинт нестерильный', 'Aseptic bandage', ['Флисовая ткань'], 6, 30)
Craft.add('Моток паракорда', 'Paracord', [*repeat('Спортивная сумка', 5), *repeat('Пучок проводов', 3),
                                          'Барс А-2607 95х18', 'Зажигалка Crickent'], 1, 248)
Craft.add('Разгрузочный жилет Сплав Тарзан М22', 'Splav Tarzan M22 Rig', ['Полиамидная ткань Кордура',
                                                                          'Ткань рипстоп'], 1, 44)
Craft.add('Липкая лента KEKТЕЙП', 'KEKTAPE duct tape', [*repeat('Монтажный скотч', 2), *repeat('Изолента', 2),
                                                        'Стеклоочиститель'], 1, 77)
Craft.add('Гофрированный шланг', 'Corrugated hose', [*repeat('Пучок проводов', 3), *repeat('Изолента', 3),
                                                     'Силиконовая трубка'], 2, 194)
# ----------------------- верстак
Craft.add('Граната "хаттабка" на базе ВОГ-25', 'VOG-25 Khattabka grenade',
          [*repeat('Запал УЗРГМ для гранат', 5), *repeat('40 мм ВОГ-25', 5)], 8, 64)

# ----------------------- пищеблок

Craft.add('Пачка сахара', 'Pack of sugar', [*repeat('Шоколад Алёнка', 2)], 1, 80)
Craft.add('Чистая Энергия', 'Max energy', ['ТарКола', 'Банка кофе Majaica', 'Бутылка воды 0.6'], 4, 204)
