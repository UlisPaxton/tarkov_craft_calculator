import browser


def repeat(item_name, count):
    """мультиплексор, возвращает словарь строк item_name, содержащий count элементов"""
    generated_list = [item_name for _ in range(0, count)]
    return generated_list


class Craft:
    browser = browser.CustomBrowser()

    craft_table = [{'name': 'Кейс для магазинов',

                    'craft_from': [*repeat('Канистра Экспедиционная топливная 0/60', 2), *repeat('Болты', 3),
                                   *repeat('Гайки', 3), 'Ножницы для резки металла'
                                   ],
                    'result_count': 1,
                    'craft_duration': 283,
                    }
                   ]
    name_matching_table = {'Канистра Экспедиционная топливная (0/60)': 'Expeditionary fuel tank (0/60)'}

    @classmethod
    def get(cls, item_name):
        try:
            return cls.name_matching_table[item_name]
        except KeyError:
            return item_name

    @classmethod
    def get_craft_element(cls, item_name):
        for element in cls.craft_table:
            if element['name'] == item_name:
                return element
        print(item_name, "нет в таблице крафта.")
        exit()

    @classmethod
    def add(cls, name, market_name, craft_from, result_count, craft_duration):

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
        """

        cls.craft_table.append({'name': name, 'craft_from': craft_from, 'result_count': result_count,
                                'craft_duration': craft_duration})
        cls.name_matching_table.update({name: market_name})

    @classmethod
    def craft(cls, item_name):
        #print(item_name, cls.craft_table.keys())
        item = cls.get_craft_element(item_name)

        try:
            #print(item)
            item_market_name = cls.name_matching_table[item['name']]
        except ValueError:
            item_market_name = item['name']

        item_sale_price = cls.browser.get_price(item_market_name)
        result_sale_price = item_sale_price * item['result_count']
        total_price = 0

        print('---------------------------------------------------------')
        for resource in item['craft_from']:
            resource_price = cls.browser.get_price(cls.get(resource))
            print(resource, resource_price)
            total_price += resource_price

        print('Крафтим', item['name'])
        print('Цена продажи:', result_sale_price, 'Цена ресурсов:', total_price)
        print('Профит:', result_sale_price - total_price)
        print('Профит в час', (result_sale_price - total_price)/item['craft_duration'] * 60)


if __name__ == '__main__':
    Craft.add('Магазин 6Л31', 'Магазин 6Л31', [*repeat('Магазин 6Л23', 4), 'Липкая лента KEKТЕЙП'], 1, 80)

    #for item in Craft.craft_table:
    #    print(item)