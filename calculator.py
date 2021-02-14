from sys import exit
from craft_table import Craft, repeat




"""
 при желании можно скорректтировать цены и провести рассчёты исходя из указанных цен
 
Craft.browser.cache.update({'Зажигалка Crickent': 12_000})
Craft.browser.cache.update({'Бензиновая зажигалка Zibbo': 18_000})
Craft.browser.cache.update({'Канистра Экспедиционная топливная (60/60)': 320_000})
Craft.browser.cache.update({'Запал УЗРГМ для гранат': 11_000})
Craft.browser.cache.update({'40 мм ВОГ-25': 16_000})
Craft.browser.cache.update({'Граната "хаттабка" на базе ВОГ-25': 22_000})
"""
""" Пример вызова крафта
# Craft.craft('Канистра Экспедиционная топливная (60/60)')
# Craft.craft('Граната "хаттабка" на базе ВОГ-25')
# Craft.craft('Водный фильтр')

"""

while True:
    for count, item in enumerate(Craft.craft_table):
        print(count, item['name'])
    try:
        item_number_to_craft = int(input('Выберите номер предмета для рассчёта:> '))
        item_to_craft = Craft.craft_table[item_number_to_craft]
        Craft.craft(item_to_craft['name'])
    except IndexError:
        print('Такого номера в списке нет.')
    except ValueError:
        print('Числовой номер, пожалуйста.')

    if input("Ещё?(Y/N)").upper() == 'N':
        exit()



