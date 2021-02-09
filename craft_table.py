def repeat(item_name, count):
    """мультиплексор, возвращает словарь строк item_name, содержащий count элементов"""
    generated_list = [item_name for _ in range(0, count)]
    return generated_list


craft_table = [{'name': 'Кейс для магазинов',
                'market_name': 'Кейс для магазинов',
                'craft_from': [*repeat('Expeditionary fuel tank (0/60)', 2), *repeat('Болты', 3),
                               *repeat('Гайки', 3), 'Ножницы для резки металла'
                               ],
                'result_count': 1,
                'craft_duration': 283,
                }
               ]


def add(name, market_name, craft_from, result_count, craft_duration):
    """Добавление структуры в таблицу крафта
    пример вызова
    add('Магазин 6Л31', 'Магазин 6Л31', [*repeat('Магазин 6Л23', 4), 'Липкая лента KEKТЕЙП'], 1, 80)
    результат
    {'name': 'Магазин 6Л31',
     'market_name': 'Магазин 6Л31',
     'craft_from': ['Магазин 6Л23', 'Магазин 6Л23', 'Магазин 6Л23',
                    'Магазин 6Л23', 'Липкая лента KEKТЕЙП'],
     'result_count': 1,
    'craft_duration': 80}

    параметр market_name предназначен для подстанвки в поисковый запрос в качестве точного указателя
     в соответствии с API и не всегда является удобочитаемым
    """
    craft_table.append({'name': name, 'market_name': market_name,
                        'craft_from': craft_from, 'result_count': result_count, 'craft_duration': craft_duration})


if __name__ == '__main__':
    add('Магазин 6Л31', 'Магазин 6Л31', [*repeat('Магазин 6Л23', 4), 'Липкая лента KEKТЕЙП'], 1, 80)

    for item in craft_table:
        print(item)